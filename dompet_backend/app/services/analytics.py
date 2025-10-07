"""Lightweight analytics helpers used during MVP development."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..core.config import settings


@dataclass
class AnalyticsEvent:
    user_id: str
    event: str
    properties: dict[str, Any]


@dataclass
class AnalyticsClient:
    """In-memory analytics collector that can be swapped for PostHog later."""

    environment: str = "development"
    events: list[AnalyticsEvent] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    configured: bool = False

    def configure(
        self,
        api_key: str | None,
        host: str | None,
        sentry_dsn: str | None,
        environment: str,
    ) -> None:  # pragma: no cover - configuration is a simple assignment
        if self.configured:
            return
        self.environment = environment or self.environment
        self.configured = True

    def track(self, *, user_id: str, event: str, properties: dict[str, Any] | None = None) -> bool:
        self.events.append(
            AnalyticsEvent(
                user_id=user_id,
                event=event,
                properties=properties or {},
            )
        )
        return True

    def capture_exception(self, error: Exception) -> None:
        self.errors.append(str(error))


analytics = AnalyticsClient()
analytics.configure(
    settings.posthog_api_key,
    settings.posthog_host,
    settings.sentry_dsn,
    settings.environment,
)
