"""FastAPI routes for the conversational layer."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ..models.conversation import ConversationMessage, ConversationResponse, MemoryUpdate, UserMemory
from ..services.conversation import ConversationService, get_memory_store
from ..services.database import get_session

router = APIRouter()


@router.post("/{user_id}/message", response_model=ConversationResponse)
def converse(
    user_id: str,
    payload: ConversationMessage,
    session=Depends(get_session),
) -> ConversationResponse:
    service = ConversationService(session, memory_store=get_memory_store())
    return service.handle_message(user_id, payload)


@router.get("/{user_id}/memory", response_model=UserMemory)
def read_memory(
    user_id: str,
    session=Depends(get_session),  # pragma: no cover - FastAPI dependency injection
) -> UserMemory:
    service = ConversationService(session, memory_store=get_memory_store())
    return service.get_memory(user_id)


@router.post("/{user_id}/memory", response_model=UserMemory)
def update_memory(
    user_id: str,
    payload: MemoryUpdate,
    session=Depends(get_session),  # pragma: no cover - FastAPI dependency injection
) -> UserMemory:
    service = ConversationService(session, memory_store=get_memory_store())
    return service.update_memory(user_id, payload)
