import pytest
from dompet_backend.app.models.beta import BetaTesterIn
from dompet_backend.app.services.beta import BetaTesterService
from dompet_backend.app.services.database import get_session, init_db


def setup_module() -> None:  # pragma: no cover - setup
    init_db()


def test_register_beta_testers_with_quota() -> None:
    session_gen = get_session()
    session = next(session_gen)
    service = BetaTesterService(session)
    service.quota = 2

    tester1 = service.register(
        BetaTesterIn(
            full_name="Ain",
            email="ain@example.com",
            persona="salaried",
        )
    )
    tester2 = service.register(
        BetaTesterIn(
            full_name="Rahman",
            email="rahman@example.com",
            persona="gig",
        )
    )

    assert tester1.id is not None
    assert tester2.id is not None

    with pytest.raises(ValueError):
        service.register(
            BetaTesterIn(
                full_name="Lim",
                email="lim@example.com",
                persona="family",
            )
        )

    try:
        next(session_gen)
    except StopIteration:
        pass
