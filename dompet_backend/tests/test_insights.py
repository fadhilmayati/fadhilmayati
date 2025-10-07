from datetime import date

from dompet_backend.app.models.transaction import TransactionIn
from dompet_backend.app.services.database import get_session, init_db
from dompet_backend.app.services.ingestion import StatementIngestionService
from dompet_backend.app.services.insights import InsightService


def setup_module() -> None:  # pragma: no cover - setup
    init_db()


def seed_transactions(session) -> None:
    ingestion = StatementIngestionService(session)
    ingestion.ingest_transactions(
        [
            TransactionIn(
                user_id="user-2",
                posted_date=date(2024, 1, 1),
                description="Salary",
                amount=6000,
                category="income",
            ),
            TransactionIn(
                user_id="user-2",
                posted_date=date(2024, 1, 5),
                description="Rent",
                amount=-1800,
                category="housing",
            ),
            TransactionIn(
                user_id="user-2",
                posted_date=date(2024, 1, 15),
                description="Utilities",
                amount=-300,
                category="utilities",
            ),
        ]
    )


def test_cashflow_summary():
    session_gen = get_session()
    session = next(session_gen)
    seed_transactions(session)
    insights = InsightService(session)

    summary = insights.cashflow_summary("user-2")

    assert summary.total_income == 6000
    assert summary.total_expense == 2100
    assert summary.net_cashflow == 3900
    assert summary.saving_rate == round(3900 / 6000, 2)

    try:
        next(session_gen)
    except StopIteration:
        pass
