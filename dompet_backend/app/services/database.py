"""Lightweight in-memory database utilities used by the MVP services."""

from __future__ import annotations

from collections.abc import Iterator
from threading import Lock

from ..models.transaction import Transaction

_TRANSACTIONS: list[Transaction] = []
_NEXT_ID = 1
_LOCK = Lock()


def init_db() -> None:
    """Reset the in-memory store. Called before tests and on app startup."""

    global _TRANSACTIONS, _NEXT_ID
    with _LOCK:
        _TRANSACTIONS = []
        _NEXT_ID = 1


class InMemorySession:
    """Session facade that mimics the parts of SQLModel used in the services."""

    def add(self, transaction: Transaction) -> None:
        global _NEXT_ID
        with _LOCK:
            if transaction.id is None:
                transaction.id = _NEXT_ID
                _NEXT_ID += 1
            _TRANSACTIONS.append(transaction)

    def commit(self) -> None:  # pragma: no cover - no-op for in-memory store
        return None

    def list_transactions(self, user_id: str) -> list[Transaction]:
        with _LOCK:
            return [tx for tx in _TRANSACTIONS if tx.user_id == user_id]

    def iter_transactions(
        self, user_id: str, *, start=None, end=None
    ) -> Iterator[Transaction]:
        with _LOCK:
            for tx in _TRANSACTIONS:
                if tx.user_id != user_id:
                    continue
                if start and tx.posted_date < start:
                    continue
                if end and tx.posted_date > end:
                    continue
                yield tx


def get_session() -> Iterator[InMemorySession]:
    """Provide a generator interface consistent with SQLModel sessions."""

    session = InMemorySession()
    yield session
