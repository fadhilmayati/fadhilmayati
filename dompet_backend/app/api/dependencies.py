"""FastAPI dependency wrappers for Dompet services."""

from fastapi import Depends, Header, HTTPException, status

from ..models.auth import AuthenticatedUser
from ..services.auth import AuthError, authenticate_bearer, get_biometric_service
from ..services.database import InMemorySession, get_session


def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> AuthenticatedUser:
    try:
        return authenticate_bearer(authorization)
    except AuthError as exc:  # pragma: no cover - HTTP bridge
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def get_biometric_service_dep(
    session: InMemorySession = Depends(get_session),
):
    return get_biometric_service(session)
