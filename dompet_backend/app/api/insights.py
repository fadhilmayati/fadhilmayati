from datetime import date

from fastapi import APIRouter, Depends, Query

from ..models.transaction import CashflowSummary
from ..services.database import get_session
from ..services.insights import InsightService

router = APIRouter()


@router.get("/{user_id}/cashflow", response_model=CashflowSummary)
def cashflow_summary(
    user_id: str,
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    session=Depends(get_session),
) -> CashflowSummary:
    service = InsightService(session)
    return service.cashflow_summary(user_id, start=start, end=end)


@router.get("/{user_id}/expense-by-category")
def expense_by_category(
    user_id: str,
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    session=Depends(get_session),
) -> dict[str, float]:
    service = InsightService(session)
    return service.expense_by_category(user_id, start=start, end=end)


@router.get("/{user_id}/recommendations")
def recommendations(
    user_id: str,
    session=Depends(get_session),
) -> dict[str, list[str]]:
    service = InsightService(session)
    summary = service.cashflow_summary(user_id)
    return {"recommendations": service.income_opportunities(summary)}
