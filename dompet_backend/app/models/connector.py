from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from typing import Literal

from .transaction import TransactionIn

ConnectorType = Literal["bank", "ewallet", "card"]


@dataclass
class Connector:
    """Represents a linked financial data source for a user."""

    user_id: str
    provider: str
    provider_type: ConnectorType
    account_name: str
    status: str = "active"
    supports_manual_entry: bool = True
    metadata: dict[str, str] | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_synced_at: datetime | None = None
    id: int | None = None


@dataclass
class ConnectorIn:
    provider: str
    provider_type: ConnectorType
    account_name: str
    supports_manual_entry: bool = True
    metadata: dict[str, str] | None = None

    def to_connector(self, user_id: str) -> Connector:
        return Connector(
            user_id=user_id,
            provider=self.provider,
            provider_type=self.provider_type,
            account_name=self.account_name,
            supports_manual_entry=self.supports_manual_entry,
            metadata=self.metadata,
        )


@dataclass
class ManualTransactionIn:
    """Manual transaction entry used for bank/e-wallet connectors."""

    posted_date: date
    description: str
    amount: float
    category: str | None = None
    account_type: str | None = None
    notes: str | None = None

    def to_transaction(self, user_id: str, connector_id: int | None = None) -> TransactionIn:
        source = "manual-entry"
        if connector_id is not None:
            source = f"manual-entry:{connector_id}"
        return TransactionIn(
            user_id=user_id,
            posted_date=self.posted_date,
            description=self.description,
            amount=self.amount,
            category=self.category,
            account_type=self.account_type,
            source_document=source,
        )
