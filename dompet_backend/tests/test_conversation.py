from datetime import date

from dompet_backend.app.models.conversation import ConversationMessage, FinancialGoal, UserProfile
from dompet_backend.app.models.transaction import TransactionIn
from dompet_backend.app.services.conversation import ConversationMemoryStore, ConversationService
from dompet_backend.app.services.database import get_session, init_db
from dompet_backend.app.services.ingestion import StatementIngestionService


def setup_module() -> None:  # pragma: no cover - setup
    init_db()


def test_conversation_requests_profile_when_missing() -> None:
    session_gen = get_session()
    session = next(session_gen)
    memory_store = ConversationMemoryStore()
    service = ConversationService(session, memory_store=memory_store)

    response = service.handle_message("user-1", ConversationMessage(message="Hello"))

    assert "collect_profile" in response.actions
    assert "need some basics" in response.message.lower()

    try:
        next(session_gen)
    except StopIteration:
        pass


def test_conversation_generates_summary_and_recommendations() -> None:
    init_db()
    session_gen = get_session()
    session = next(session_gen)

    ingestion_service = StatementIngestionService(session)
    ingestion_service.ingest_transactions(
        [
            TransactionIn(
                user_id="user-42",
                posted_date=date(2024, 1, 1),
                description="Salary",
                amount=5000.0,
                category="income",
            ),
            TransactionIn(
                user_id="user-42",
                posted_date=date(2024, 1, 5),
                description="Rent",
                amount=-1500.0,
                category="housing",
            ),
            TransactionIn(
                user_id="user-42",
                posted_date=date(2024, 1, 10),
                description="Groceries",
                amount=-600.0,
                category="food",
            ),
        ]
    )

    memory_store = ConversationMemoryStore()
    service = ConversationService(session, memory_store=memory_store)

    response = service.handle_message(
        "user-42",
        ConversationMessage(
            message="Can you give me a cashflow summary and recommendations?",
            profile=UserProfile(name="Aisha", age=32, household_size=3),
            goals=[FinancialGoal(name="Emergency fund", target_amount=12000.0)],
        ),
    )

    assert "cashflow_summary" in response.actions
    assert "recommendations" in response.actions
    assert "cashflow summary" in response.message.lower()
    assert "tailored" in response.message.lower()
    assert response.memory.profile is not None
    assert response.memory.profile.name == "Aisha"
    assert len(response.memory.goals) == 1
    assert response.memory.conversation_history[-1].role == "assistant"

    try:
        next(session_gen)
    except StopIteration:
        pass
