from datetime import date

from dompet_backend.app.models.transaction import TransactionIn
from dompet_backend.app.services.database import get_session, init_db
from dompet_backend.app.services.ingestion import StatementIngestionService


def setup_module() -> None:  # pragma: no cover - setup
    init_db()


def test_ingest_transactions() -> None:
    session_gen = get_session()
    session = next(session_gen)
    service = StatementIngestionService(session)
    payload = [
        TransactionIn(
            user_id="user-1",
            posted_date=date(2024, 1, 1),
            description="Salary",
            amount=5000.0,
            category="income",
        ),
        TransactionIn(
            user_id="user-1",
            posted_date=date(2024, 1, 2),
            description="Groceries",
            amount=-200.0,
            category="food",
        ),
    ]

    inserted = service.ingest_transactions(payload)
    assert inserted == 2

    records = service.list_transactions("user-1")
    assert len(records) == 2
    assert records[0].description == "Salary"
    assert records[1].amount == -200.0

    try:
        next(session_gen)
    except StopIteration:
        pass
