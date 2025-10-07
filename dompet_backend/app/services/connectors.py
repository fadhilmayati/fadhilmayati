"""Connector management service handling bank and e-wallet integrations."""

from __future__ import annotations

from datetime import datetime, timezone

from ..models.connector import Connector, ConnectorIn, ManualTransactionIn
from ..models.transaction import Transaction
from .analytics import analytics
from .database import InMemorySession
from .ingestion import StatementIngestionService


class ConnectorService:
    """Encapsulates connector lifecycle and manual transaction entry."""

    def __init__(self, session: InMemorySession):
        self.session = session
        self.ingestion = StatementIngestionService(session)

    def register_connector(self, user_id: str, payload: ConnectorIn) -> Connector:
        connector = payload.to_connector(user_id)
        connector = self.session.add_connector(connector)
        analytics.track(
            user_id=user_id,
            event="connector_registered",
            properties={
                "provider": connector.provider,
                "type": connector.provider_type,
            },
        )
        return connector

    def list_connectors(self, user_id: str) -> list[Connector]:
        return self.session.list_connectors(user_id)

    def record_sync(self, connector_id: int) -> Connector:
        connector = self.session.touch_connector(
            connector_id,
            timestamp=datetime.now(timezone.utc),
        )
        analytics.track(
            user_id=connector.user_id,
            event="connector_synced",
            properties={"connector_id": connector_id},
        )
        return connector

    def record_manual_entry(
        self,
        user_id: str,
        payload: ManualTransactionIn,
        *,
        connector_id: int | None = None,
    ) -> Transaction:
        transaction_in = payload.to_transaction(user_id, connector_id)
        self.ingestion.ingest_transactions([transaction_in])
        transaction = self.session.list_transactions(user_id)[-1]
        analytics.track(
            user_id=user_id,
            event="manual_transaction_recorded",
            properties={
                "amount": transaction.amount,
                "category": transaction.category,
                "connector_id": connector_id,
            },
        )
        return transaction
