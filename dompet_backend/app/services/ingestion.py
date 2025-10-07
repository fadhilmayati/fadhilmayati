from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime
from io import StringIO
from typing import TYPE_CHECKING, Any, Protocol

import csv

from ..models.transaction import Transaction, TransactionIn
from .analytics import analytics
from .database import InMemorySession

if TYPE_CHECKING:  # pragma: no cover - only imported for FastAPI compatibility
    from fastapi import UploadFile  # type: ignore
else:

    class UploadFile(Protocol):  # pragma: no cover - runtime protocol definition
        filename: str | None
        content_type: str | None

        @property
        def file(self) -> Any: ...

SUPPORTED_MIME_TYPES = {
    "text/csv",
    "application/vnd.ms-excel",
    "application/octet-stream",
}


class StatementIngestionService:
    def __init__(self, session: InMemorySession):
        self.session = session

    def ingest_transactions(self, transactions: Iterable[TransactionIn]) -> int:
        count = 0
        user_id: str | None = None
        for tx in transactions:
            record = tx.to_transaction()
            self.session.add(record)
            count += 1
            user_id = record.user_id
        self.session.commit()
        if user_id:
            analytics.track(
                user_id=user_id,
                event="transactions_ingested",
                properties={"count": count},
            )
        return count

    def parse_statement(self, user_id: str, file: UploadFile) -> list[TransactionIn]:
        content_type = (file.content_type or "text/csv").lower()
        if content_type not in SUPPORTED_MIME_TYPES:
            raise ValueError("Unsupported file type")

        raw_bytes = file.file.read()
        text = raw_bytes.decode("utf-8-sig")
        reader = csv.DictReader(StringIO(text))
        if reader.fieldnames is None:
            raise ValueError("Missing header row")

        headers = {name.lower() for name in reader.fieldnames}
        required_columns = {"date", "description", "amount"}
        if not required_columns.issubset(headers):
            raise ValueError("Missing columns: date, description, amount")

        transactions: list[TransactionIn] = []
        for row in reader:
            normalised_row = {key.lower(): value for key, value in row.items()}
            posted_date = self._parse_date(normalised_row.get("date"))
            description = str(normalised_row.get("description", "")).strip()
            amount_raw = normalised_row.get("amount", 0) or 0
            amount = float(amount_raw)
            category = normalised_row.get("category")
            account_type = normalised_row.get("account_type")

            transactions.append(
                TransactionIn(
                    user_id=user_id,
                    posted_date=posted_date,
                    description=description,
                    amount=amount,
                    category=str(category).strip() if category else None,
                    account_type=str(account_type).strip() if account_type else None,
                    source_document=file.filename,
                )
            )

        return transactions

    def list_transactions(self, user_id: str) -> list[Transaction]:
        return self.session.list_transactions(user_id)

    @staticmethod
    def _parse_date(value: Any) -> date:
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
        raise ValueError(f"Unrecognised date format: {value}")
