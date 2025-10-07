"""Authentication-facing API endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..api.dependencies import get_biometric_service_dep, get_current_user
from ..models.auth import AuthenticatedUser, BiometricDevice
from ..services.auth import AuthError, BiometricService, _supabase_auth

router = APIRouter()


class MagicLinkVerificationRequest(BaseModel):
    access_token: str


class MagicLinkVerificationResponse(BaseModel):
    user_id: str
    email: str
    phone: str | None = None
    is_verified: bool


class BiometricEnrollRequest(BaseModel):
    device_id: str
    public_key: str


class BiometricVerifyRequest(BaseModel):
    device_id: str


@router.post("/magic-link/verify", response_model=MagicLinkVerificationResponse)
def verify_magic_link(
    payload: MagicLinkVerificationRequest,
) -> MagicLinkVerificationResponse:
    try:
        user = _supabase_auth.verify_access_token(payload.access_token)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
    return MagicLinkVerificationResponse(
        user_id=user.user_id,
        email=user.email,
        phone=user.phone,
        is_verified=user.is_verified,
    )


@router.post("/biometric/enrol", response_model=BiometricDevice)
def enrol_biometric_device(
    payload: BiometricEnrollRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    service: BiometricService = Depends(get_biometric_service_dep),
) -> BiometricDevice:
    return service.enrol_device(
        user_id=current_user.user_id,
        device_id=payload.device_id,
        public_key=payload.public_key,
    )


@router.post("/biometric/verify", response_model=BiometricDevice)
def verify_biometric_device(
    payload: BiometricVerifyRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    service: BiometricService = Depends(get_biometric_service_dep),
) -> BiometricDevice:
    return service.verify_device(
        user_id=current_user.user_id,
        device_id=payload.device_id,
    )
