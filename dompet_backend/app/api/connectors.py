"""API routes for managing bank and e-wallet connectors."""

from __future__ import annotations

from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..api.dependencies import get_current_user
from ..models.connector import Connector
from ..models.transaction import Transaction
from ..services.connectors import ConnectorService
from ..services.database import get_session

router = APIRouter()


class ConnectorPayload(BaseModel):
    provider: str
    provider_type: Literal["bank", "ewallet", "card"]
    account_name: str
    supports_manual_entry: bool = True
    metadata: dict[str, str] | None = None

    def to_dataclass(self):
        from ..models.connector import ConnectorIn

        return ConnectorIn(
            provider=self.provider,
            provider_type=self.provider_type,
            account_name=self.account_name,
            supports_manual_entry=self.supports_manual_entry,
            metadata=self.metadata,
        )


class ManualEntryPayload(BaseModel):
    posted_date: date
    description: str
    amount: float
    category: str | None = None
    account_type: str | None = None
    notes: str | None = None

    def to_dataclass(self):
        from ..models.connector import ManualTransactionIn

        return ManualTransactionIn(
            posted_date=self.posted_date,
            description=self.description,
            amount=self.amount,
            category=self.category,
            account_type=self.account_type,
            notes=self.notes,
        )


@router.post("/{user_id}", response_model=Connector)
def register_connector(
    user_id: str,
    payload: ConnectorPayload,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
) -> Connector:
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User mismatch")
    service = ConnectorService(session)
    connector = service.register_connector(user_id, payload.to_dataclass())
    return connector


@router.get("/{user_id}", response_model=list[Connector])
def list_connectors(
    user_id: str,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
) -> list[Connector]:
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User mismatch")
    service = ConnectorService(session)
    return service.list_connectors(user_id)


@router.post("/{user_id}/{connector_id}/sync", response_model=Connector)
def record_sync(
    user_id: str,
    connector_id: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
) -> Connector:
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User mismatch")
    service = ConnectorService(session)
    connector = service.record_sync(connector_id)
    if connector.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connector not found")
    return connector


@router.post("/{user_id}/{connector_id}/manual", response_model=Transaction)
def record_manual_transaction(
    user_id: str,
    connector_id: int,
    payload: ManualEntryPayload,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
) -> Transaction:
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User mismatch")
    service = ConnectorService(session)
    connector_list = service.list_connectors(user_id)
    if not any(conn.id == connector_id for conn in connector_list):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connector not found")
    return service.record_manual_entry(
        user_id,
        payload.to_dataclass(),
        connector_id=connector_id,
    )
