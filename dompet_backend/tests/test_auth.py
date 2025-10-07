import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone

import pytest

from dompet_backend.app.services import auth
from dompet_backend.app.services.auth import BiometricService, SupabaseAuthService
from dompet_backend.app.services.database import get_session, init_db


def setup_module() -> None:  # pragma: no cover - setup
    init_db()


def test_verify_supabase_token() -> None:
    secret = "secret-key"
    service = SupabaseAuthService(secret=secret)
    token = _generate_hs256(
        {
            "sub": "user-123",
            "email": "user@example.com",
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "email_confirmed": True,
        },
        secret,
    )

    user = service.verify_access_token(token)
    assert user.user_id == "user-123"
    assert user.email == "user@example.com"


def test_biometric_enrolment_and_verification() -> None:
    session_gen = get_session()
    session = next(session_gen)
    service = BiometricService(session)
    enrolled = service.enrol_device(user_id="user-123", device_id="iphone", public_key="pk")
    assert enrolled.device_id == "iphone"

    verified = service.verify_device(user_id="user-123", device_id="iphone")
    assert verified.last_authenticated_at is not None

    with pytest.raises(auth.AuthError):
        service.verify_device(user_id="user-123", device_id="android")

    try:
        next(session_gen)
    except StopIteration:
        pass


def test_get_current_user_bypass(monkeypatch: pytest.MonkeyPatch) -> None:
    original = auth.settings.auth_bypass
    monkeypatch.setattr(auth.settings, "auth_bypass", True)
    user = auth.authenticate_bearer(None)
    assert user.user_id == "local-dev"
    monkeypatch.setattr(auth.settings, "auth_bypass", original)


def _generate_hs256(payload: dict[str, object], secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _b64encode(header)
    payload_b64 = _b64encode(payload)
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def _b64encode(data: dict[str, object]) -> str:
    json_bytes = json.dumps(data, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(json_bytes).rstrip(b"=").decode()
