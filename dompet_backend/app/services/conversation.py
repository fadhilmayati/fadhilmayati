"""Conversation planning and memory services for Dompet."""

from __future__ import annotations

from collections.abc import Iterable
from threading import Lock

from ..models.conversation import (
    ConversationMessage,
    ConversationResponse,
    ConversationTurn,
    FinancialGoal,
    MemoryUpdate,
    Obligation,
    UserMemory,
    UserProfile,
)
from .database import InMemorySession
from .insights import InsightService


class ConversationMemoryStore:
    """Thread-safe in-memory store for conversation memories."""

    def __init__(self) -> None:
        self._store: dict[str, UserMemory] = {}
        self._lock = Lock()

    def get_memory(self, user_id: str) -> UserMemory:
        with self._lock:
            memory = self._store.get(user_id)
            if memory is None:
                memory = UserMemory(user_id=user_id)
                self._store[user_id] = memory
            return memory

    def update_memory(
        self,
        user_id: str,
        *,
        profile: UserProfile | None = None,
        goals: Iterable[FinancialGoal] | None = None,
        obligations: Iterable[Obligation] | None = None,
    ) -> UserMemory:
        with self._lock:
            memory = self._store.get(user_id)
            if memory is None:
                memory = UserMemory(user_id=user_id)
            if profile is not None:
                memory.profile = profile
            if goals is not None:
                merged = {goal.name.lower(): goal for goal in memory.goals}
                for goal in goals:
                    merged[goal.name.lower()] = goal
                memory.goals = list(merged.values())
            if obligations is not None:
                merged = {obligation.name.lower(): obligation for obligation in memory.obligations}
                for obligation in obligations:
                    merged[obligation.name.lower()] = obligation
                memory.obligations = list(merged.values())
            self._store[user_id] = memory
            return memory

    def append_turn(self, user_id: str, turn: ConversationTurn) -> UserMemory:
        with self._lock:
            memory = self._store.get(user_id)
            if memory is None:
                memory = UserMemory(user_id=user_id)
            history = list(memory.conversation_history)
            history.append(turn)
            memory.conversation_history = history[-20:]
            self._store[user_id] = memory
            return memory


class ChatPlanner:
    """Very small rule-based planner with deterministic fallbacks."""

    def plan(self, message: str, memory: UserMemory) -> list[str]:
        lowered = message.lower()
        actions: list[str] = []

        if memory.profile is None:
            actions.append("collect_profile")

        if any(keyword in lowered for keyword in ("cashflow", "summary", "income", "spend", "expense")):
            if "cashflow_summary" not in actions:
                actions.append("cashflow_summary")

        if any(keyword in lowered for keyword in ("category", "breakdown", "spending")):
            actions.append("expense_breakdown")

        if any(keyword in lowered for keyword in ("recommend", "advice", "plan", "goal")):
            actions.append("recommendations")

        if not actions:
            actions.append("chit_chat")

        return actions


class ConversationService:
    """Coordinates planning, memory and insights for a conversation."""

    def __init__(
        self,
        session: InMemorySession,
        *,
        memory_store: ConversationMemoryStore,
        planner: ChatPlanner | None = None,
    ) -> None:
        self.session = session
        self.memory_store = memory_store
        self.planner = planner or ChatPlanner()
        self.insights = InsightService(session)

    def handle_message(self, user_id: str, payload: ConversationMessage) -> ConversationResponse:
        # Update memory first based on structured payload information.
        if payload.profile or payload.goals or payload.obligations:
            memory = self.memory_store.update_memory(
                user_id,
                profile=payload.profile,
                goals=payload.goals,
                obligations=payload.obligations,
            )
        else:
            memory = self.memory_store.get_memory(user_id)

        actions = self.planner.plan(payload.message, memory)
        responses: list[str] = []

        self.memory_store.append_turn(
            user_id,
            ConversationTurn(role="user", content=payload.message),
        )

        if "collect_profile" in actions and memory.profile is None:
            responses.append(
                "To personalise your financial plan I need some basics like your monthly income, household size, and key goals."
            )

        if "cashflow_summary" in actions:
            summary = self.insights.cashflow_summary(user_id)
            responses.append(
                "Cashflow summary: income RM{income:.2f}, expenses RM{expense:.2f}, net RM{net:.2f} with a saving rate of {rate:.0%}.".format(
                    income=summary.total_income,
                    expense=summary.total_expense,
                    net=summary.net_cashflow,
                    rate=summary.saving_rate,
                )
            )

        if "expense_breakdown" in actions:
            breakdown = self.insights.expense_by_category(user_id)
            if breakdown:
                categories = ", ".join(f"{name}: RM{amount:.2f}" for name, amount in breakdown.items())
                responses.append(f"Top spending categories: {categories}.")
            else:
                responses.append("I don't have any expense records yet to analyse categories.")

        if "recommendations" in actions:
            summary = self.insights.cashflow_summary(user_id)
            recs = self.insights.income_opportunities(summary)
            if recs:
                bullet_points = "\n".join(f"- {rec}" for rec in recs)
                responses.append(f"Here are some tailored next steps:\n{bullet_points}")
            else:
                responses.append("You're on track! I'll keep monitoring for new opportunities.")

        if "chit_chat" in actions and not responses:
            responses.append("I'm here to help with your Malaysian personal finance questions whenever you're ready.")

        assistant_turn = ConversationTurn(
            role="assistant",
            content="\n".join(responses) if responses else "Let me know how I can assist with your finances.",
            intent=";".join(actions),
        )
        memory = self.memory_store.append_turn(user_id, assistant_turn)

        return ConversationResponse(
            message=assistant_turn.content,
            actions=actions,
            memory=memory,
        )

    def update_memory(self, user_id: str, payload: MemoryUpdate) -> UserMemory:
        return self.memory_store.update_memory(
            user_id,
            profile=payload.profile,
            goals=payload.goals,
            obligations=payload.obligations,
        )

    def get_memory(self, user_id: str) -> UserMemory:
        return self.memory_store.get_memory(user_id)


_MEMORY_STORE = ConversationMemoryStore()


def get_memory_store() -> ConversationMemoryStore:
    """Return the singleton in-memory memory store."""

    return _MEMORY_STORE
