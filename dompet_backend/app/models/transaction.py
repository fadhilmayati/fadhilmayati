from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Transaction:
    """Persisted transaction record used by the insights services."""

    user_id: str
    posted_date: date
    description: str
    amount: float
    category: str = "uncategorised"
    account_type: str = "unknown"
    source_document: str | None = None
    id: Optional[int] = None


@dataclass
class TransactionIn:
    """Input transaction payload typically coming from statement ingestion."""

    user_id: str
    posted_date: date
    description: str
    amount: float
    category: str | None = None
    account_type: str | None = None
    source_document: str | None = None

    def to_transaction(self) -> Transaction:
        """Convert the input payload into a persisted transaction instance."""

        return Transaction(
            user_id=self.user_id,
            posted_date=self.posted_date,
            description=self.description,
            amount=self.amount,
            category=self.category or "uncategorised",
            account_type=self.account_type or "unknown",
            source_document=self.source_document,
        )


@dataclass
class CashflowSummary:
    total_income: float
    total_expense: float
    net_cashflow: float
    saving_rate: float
