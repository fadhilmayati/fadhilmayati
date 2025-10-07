"""Routes to coordinate the closed beta cohort."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..api.dependencies import get_current_user
from ..models.beta import BetaTester, BetaTesterIn
from ..services.beta import BetaTesterService
from ..services.database import get_session

router = APIRouter()


class BetaTesterPayload(BaseModel):
    full_name: str
    email: str
    persona: str
    preferred_channel: str = "whatsapp"
    session_scheduled_for: date | None = None

    def to_dataclass(self) -> BetaTesterIn:
        return BetaTesterIn(
            full_name=self.full_name,
            email=self.email,
            persona=self.persona,
            preferred_channel=self.preferred_channel,
            session_scheduled_for=self.session_scheduled_for,
        )


class FeedbackPayload(BaseModel):
    feedback: str


@router.post("/testers", response_model=BetaTester)
def register_tester(
    payload: BetaTesterPayload,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
) -> BetaTester:
    if current_user.user_id != "local-dev" and not current_user.email.endswith("@dompet.app"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    service = BetaTesterService(session)
    tester = service.register(payload.to_dataclass())
    if payload.session_scheduled_for:
        service.schedule_session(tester.id or 0, payload.session_scheduled_for)
    return tester


@router.get("/testers", response_model=list[BetaTester])
def list_testers(
    session=Depends(get_session),
    current_user=Depends(get_current_user),
) -> list[BetaTester]:
    if current_user.user_id != "local-dev" and not current_user.email.endswith("@dompet.app"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    service = BetaTesterService(session)
    return service.list_testers()


@router.post("/testers/{tester_id}/feedback", response_model=BetaTester)
def capture_feedback(
    tester_id: int,
    payload: FeedbackPayload,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
) -> BetaTester:
    if current_user.user_id != "local-dev" and not current_user.email.endswith("@dompet.app"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    service = BetaTesterService(session)
    return service.record_feedback(tester_id, payload.feedback)
