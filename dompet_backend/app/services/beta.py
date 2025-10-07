"""Closed beta participant management services."""

from __future__ import annotations

from datetime import date

from ..core.config import settings
from ..models.beta import BetaTester, BetaTesterIn
from .analytics import analytics
from .database import InMemorySession


class BetaTesterService:
    def __init__(self, session: InMemorySession):
        self.session = session
        self.quota = settings.beta_testers_target

    def register(self, payload: BetaTesterIn) -> BetaTester:
        testers = self.session.list_beta_testers()
        if len(testers) >= self.quota:
            raise ValueError("Beta tester quota reached")
        tester = payload.to_beta_tester()
        tester = self.session.add_beta_tester(tester)
        analytics.track(
            user_id=tester.email,
            event="beta_tester_registered",
            properties={
                "persona": tester.persona,
                "channel": tester.preferred_channel,
            },
        )
        return tester

    def list_testers(self) -> list[BetaTester]:
        return self.session.list_beta_testers()

    def record_feedback(self, tester_id: int, feedback: str) -> BetaTester:
        tester = self.session.update_beta_tester(tester_id, feedback=feedback)
        analytics.track(
            user_id=tester.email,
            event="beta_feedback_recorded",
            properties={"tester_id": tester_id},
        )
        return tester

    def schedule_session(self, tester_id: int, when: date) -> BetaTester:
        return self.session.update_beta_tester(
            tester_id,
            feedback=None,
            session_date=when,
        )
