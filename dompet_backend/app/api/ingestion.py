from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from ..models.transaction import Transaction, TransactionIn
from ..services.database import get_session
from ..services.ingestion import StatementIngestionService

router = APIRouter()


@router.post("/{user_id}/transactions")
def ingest_transactions(
    user_id: str,
    payload: list[TransactionIn],
    session=Depends(get_session),
) -> dict[str, int]:
    service = StatementIngestionService(session)
    inserted = service.ingest_transactions(payload)
    return {"inserted": inserted}


@router.post("/{user_id}/upload")
def upload_statement(
    user_id: str,
    file: UploadFile = File(...),
    session=Depends(get_session),
) -> dict[str, int]:
    service = StatementIngestionService(session)
    try:
        transactions = service.parse_statement(user_id, file)
    except ValueError as exc:  # pragma: no cover - validation error
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    inserted = service.ingest_transactions(transactions)
    return {"inserted": inserted}


@router.get("/{user_id}/transactions", response_model=list[Transaction])
def list_transactions(user_id: str, session=Depends(get_session)) -> list[Transaction]:
    service = StatementIngestionService(session)
    return service.list_transactions(user_id)
