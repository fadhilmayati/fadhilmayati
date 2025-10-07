from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AuthenticatedUser:
    """Representation of an authenticated Dompet user."""

    user_id: str
    email: str
    phone: str | None = None
    is_verified: bool = True
    issued_at: datetime | None = None


@dataclass
class BiometricDevice:
    """Registered biometric device metadata for secure re-authentication."""

    user_id: str
    device_id: str
    public_key: str
    enrolled_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_authenticated_at: datetime | None = None

    def touch(self) -> None:
        self.last_authenticated_at = datetime.now(timezone.utc)
