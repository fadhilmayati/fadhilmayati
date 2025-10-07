from datetime import date

import pytest

from dompet_backend.app.models.connector import ConnectorIn, ManualTransactionIn
from dompet_backend.app.services.connectors import ConnectorService
from dompet_backend.app.services.database import get_session, init_db


def setup_module() -> None:  # pragma: no cover - setup
    init_db()


def test_register_and_manual_entry() -> None:
    session_gen = get_session()
    session = next(session_gen)
    service = ConnectorService(session)
    connector = service.register_connector(
        "user-1",
        ConnectorIn(
            provider="Maybank",
            provider_type="bank",
            account_name="Savings",
        ),
    )
    assert connector.id is not None

    manual_entry = ManualTransactionIn(
        posted_date=date(2024, 5, 1),
        description="Cash deposit",
        amount=1500.0,
        category="income",
        account_type="cash",
    )
    transaction = service.record_manual_entry("user-1", manual_entry, connector_id=connector.id)

    assert transaction.amount == 1500.0
    assert transaction.source_document == f"manual-entry:{connector.id}"

    try:
        next(session_gen)
    except StopIteration:
        pass


def test_record_sync_unknown_connector() -> None:
    session_gen = get_session()
    session = next(session_gen)
    service = ConnectorService(session)
    with pytest.raises(ValueError):
        service.record_sync(999)

    try:
        next(session_gen)
    except StopIteration:
        pass
