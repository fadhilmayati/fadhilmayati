"""Conversation and memory models for the Dompet conversational layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Literal


@dataclass
class FinancialGoal:
    """Represents a long or short term financial objective."""

    name: str
    target_amount: float | None = None
    target_date: date | None = None
    priority: Literal["low", "medium", "high"] = "medium"
    notes: str | None = None


@dataclass
class Obligation:
    """Recurring payment or liability that the user must service."""

    name: str
    amount: float
    cadence: Literal["weekly", "monthly", "quarterly", "yearly"] = "monthly"
    category: str | None = None


@dataclass
class IncomeStream:
    """Represents a source of income for the household."""

    name: str
    cadence: Literal["weekly", "biweekly", "monthly", "ad-hoc"] = "monthly"
    amount: float | None = None


@dataclass
class UserProfile:
    """Key profile attributes used to personalise recommendations."""

    name: str
    age: int | None = None
    household_size: int | None = None
    location: str | None = None
    income_streams: list[IncomeStream] = field(default_factory=list)
    risk_appetite: Literal["conservative", "balanced", "aggressive"] = "balanced"


@dataclass
class ConversationTurn:
    """Single exchange in the conversation transcript."""

    role: Literal["user", "assistant", "system"]
    content: str
    intent: str | None = None


@dataclass
class UserMemory:
    """Persistent memory bundle for a given user."""

    user_id: str
    profile: UserProfile | None = None
    goals: list[FinancialGoal] = field(default_factory=list)
    obligations: list[Obligation] = field(default_factory=list)
    conversation_history: list[ConversationTurn] = field(default_factory=list)


@dataclass
class ConversationMessage:
    """Inbound message from any conversational channel."""

    message: str
    channel: Literal["chat", "voice", "email"] = "chat"
    profile: UserProfile | None = None
    goals: list[FinancialGoal] | None = None
    obligations: list[Obligation] | None = None


@dataclass
class MemoryUpdate:
    """Explicit memory update payload via API."""

    profile: UserProfile | None = None
    goals: list[FinancialGoal] | None = None
    obligations: list[Obligation] | None = None


@dataclass
class ConversationResponse:
    """Response returned to the client after the planner executes."""

    message: str
    actions: list[str]
    memory: UserMemory
