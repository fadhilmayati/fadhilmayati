from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timezone


@dataclass
class BetaTester:
    """Lightweight record tracking closed beta participants."""

    full_name: str
    email: str
    persona: str
    preferred_channel: str
    invited_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    session_scheduled_for: date | None = None
    feedback_notes: str | None = None
    id: int | None = None


@dataclass
class BetaTesterIn:
    full_name: str
    email: str
    persona: str
    preferred_channel: str = "whatsapp"
    session_scheduled_for: date | None = None

    def to_beta_tester(self) -> BetaTester:
        return BetaTester(
            full_name=self.full_name,
            email=self.email.lower(),
            persona=self.persona,
            preferred_channel=self.preferred_channel,
            session_scheduled_for=self.session_scheduled_for,
        )
