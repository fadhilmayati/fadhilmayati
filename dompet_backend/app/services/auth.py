"""Supabase authentication and biometric enrollment helpers."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any

from ..core.config import settings
from ..models.auth import AuthenticatedUser, BiometricDevice
from .database import InMemorySession


class AuthError(Exception):
    """Raised when authentication fails."""


class SupabaseAuthService:
    def __init__(
        self,
        *,
        secret: str,
        audience: str | None = None,
    ) -> None:
        self.secret = secret
        self.audience = audience

    def verify_access_token(self, token: str) -> AuthenticatedUser:
        payload = self._decode_hs256(token)

        user_id = payload.get("sub")
        email = payload.get("email")
        if not user_id or not email:
            raise AuthError("Token missing required claims")

        issued_at_raw = payload.get("iat")
        issued_at = (
            datetime.fromtimestamp(issued_at_raw, tz=timezone.utc)
            if isinstance(issued_at_raw, (int, float))
            else None
        )
        phone = payload.get("phone")
        email_confirmed = payload.get("email_confirmed", True)
        return AuthenticatedUser(
            user_id=str(user_id),
            email=str(email),
            phone=str(phone) if phone else None,
            is_verified=bool(email_confirmed),
            issued_at=issued_at,
        )

    def _decode_hs256(self, token: str) -> dict[str, Any]:
        try:
            header_b64, payload_b64, signature_b64 = token.split(".")
        except ValueError as exc:  # pragma: no cover - defensive
            raise AuthError("Invalid token format") from exc

        header = self._decode_segment(header_b64)
        if header.get("alg") != "HS256":
            raise AuthError("Unsupported JWT algorithm")

        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = self._b64decode(signature_b64)
        expected = hmac.new(self.secret.encode(), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            raise AuthError("Invalid Supabase access token")

        payload = self._decode_segment(payload_b64)
        if self.audience and payload.get("aud") not in {self.audience, None}:
            raise AuthError("Invalid audience")
        return payload

    @staticmethod
    def _decode_segment(segment: str) -> dict[str, Any]:
        data = SupabaseAuthService._b64decode(segment)
        try:
            return json.loads(data)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise AuthError("Malformed token payload") from exc

    @staticmethod
    def _b64decode(segment: str) -> bytes:
        padding = "=" * (-len(segment) % 4)
        return base64.urlsafe_b64decode(segment + padding)


class BiometricService:
    def __init__(self, session: InMemorySession):
        self.session = session

    def enrol_device(self, *, user_id: str, device_id: str, public_key: str) -> BiometricDevice:
        device = BiometricDevice(
            user_id=user_id,
            device_id=device_id,
            public_key=public_key,
        )
        return self.session.upsert_biometric_device(device)

    def verify_device(self, *, user_id: str, device_id: str) -> BiometricDevice:
        device = self.session.get_biometric_device(user_id, device_id)
        if device is None:
            raise AuthError("Biometric device not found")
        return self.session.touch_biometric_device(user_id, device_id)


_supabase_auth = SupabaseAuthService(
    secret=settings.supabase_jwt_secret,
    audience=settings.supabase_jwt_audience,
)


def authenticate_bearer(authorization: str | None) -> AuthenticatedUser:
    if settings.auth_bypass:
        return AuthenticatedUser(user_id="local-dev", email="local@dompet.app")

    if not authorization:
        raise AuthError("Missing Authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AuthError("Expected Bearer token")
    return _supabase_auth.verify_access_token(token)


def get_biometric_service(session: InMemorySession) -> BiometricService:
    return BiometricService(session)
