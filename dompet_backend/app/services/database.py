"""Lightweight in-memory database utilities used by the MVP services."""

from __future__ import annotations

from collections.abc import Iterator
from threading import Lock

from dataclasses import replace
from datetime import date, datetime, timezone

from ..models.auth import BiometricDevice
from ..models.beta import BetaTester
from ..models.connector import Connector
from ..models.transaction import Transaction

_TRANSACTIONS: list[Transaction] = []
_NEXT_ID = 1
_CONNECTORS: list[Connector] = []
_CONNECTOR_NEXT_ID = 1
_BETA_TESTERS: list[BetaTester] = []
_BETA_TESTER_NEXT_ID = 1
_BIOMETRIC_DEVICES: list[BiometricDevice] = []
_LOCK = Lock()


def init_db() -> None:
    """Reset the in-memory store. Called before tests and on app startup."""

    global _TRANSACTIONS, _NEXT_ID, _CONNECTORS, _CONNECTOR_NEXT_ID
    global _BETA_TESTERS, _BETA_TESTER_NEXT_ID, _BIOMETRIC_DEVICES
    with _LOCK:
        _TRANSACTIONS = []
        _NEXT_ID = 1
        _CONNECTORS = []
        _CONNECTOR_NEXT_ID = 1
        _BETA_TESTERS = []
        _BETA_TESTER_NEXT_ID = 1
        _BIOMETRIC_DEVICES = []


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

    # Connector helpers -------------------------------------------------

    def add_connector(self, connector: Connector) -> Connector:
        global _CONNECTOR_NEXT_ID
        with _LOCK:
            if connector.id is None:
                connector.id = _CONNECTOR_NEXT_ID
                _CONNECTOR_NEXT_ID += 1
            _CONNECTORS.append(connector)
            return connector

    def list_connectors(self, user_id: str) -> list[Connector]:
        with _LOCK:
            return [item for item in _CONNECTORS if item.user_id == user_id]

    def touch_connector(self, connector_id: int, *, timestamp: datetime | None = None) -> Connector:
        with _LOCK:
            for idx, connector in enumerate(_CONNECTORS):
                if connector.id == connector_id:
                    updated = replace(
                        connector,
                        last_synced_at=timestamp or datetime.now(timezone.utc),
                    )
                    _CONNECTORS[idx] = updated
                    return updated
        raise ValueError(f"Connector {connector_id} not found")

    # Beta tester helpers ------------------------------------------------

    def add_beta_tester(self, tester: BetaTester) -> BetaTester:
        global _BETA_TESTER_NEXT_ID
        with _LOCK:
            if tester.id is None:
                tester.id = _BETA_TESTER_NEXT_ID
                _BETA_TESTER_NEXT_ID += 1
            _BETA_TESTERS.append(tester)
            return tester

    def list_beta_testers(self) -> list[BetaTester]:
        with _LOCK:
            return list(_BETA_TESTERS)

    def update_beta_tester(
        self,
        tester_id: int,
        *,
        feedback: str | None = None,
        session_date: date | None = None,
    ) -> BetaTester:
        with _LOCK:
            for idx, tester in enumerate(_BETA_TESTERS):
                if tester.id == tester_id:
                    updated = replace(tester, feedback_notes=feedback)
                    if session_date is not None:
                        updated = replace(
                            updated,
                            session_scheduled_for=session_date,
                        )
                    _BETA_TESTERS[idx] = updated
                    return updated
        raise ValueError(f"Tester {tester_id} not found")

    # Biometric helpers --------------------------------------------------

    def upsert_biometric_device(self, device: BiometricDevice) -> BiometricDevice:
        with _LOCK:
            for idx, existing in enumerate(_BIOMETRIC_DEVICES):
                if (
                    existing.user_id == device.user_id
                    and existing.device_id == device.device_id
                ):
                    _BIOMETRIC_DEVICES[idx] = device
                    return device
            _BIOMETRIC_DEVICES.append(device)
            return device

    def get_biometric_device(
        self, user_id: str, device_id: str
    ) -> BiometricDevice | None:
        with _LOCK:
            for device in _BIOMETRIC_DEVICES:
                if device.user_id == user_id and device.device_id == device_id:
                    return device
        return None

    def touch_biometric_device(self, user_id: str, device_id: str) -> BiometricDevice:
        with _LOCK:
            for idx, device in enumerate(_BIOMETRIC_DEVICES):
                if device.user_id == user_id and device.device_id == device_id:
                    device.touch()
                    _BIOMETRIC_DEVICES[idx] = device
                    return device
        raise ValueError(f"Device {device_id} not found for user {user_id}")


def get_session() -> Iterator[InMemorySession]:
    """Provide a generator interface consistent with SQLModel sessions."""

    session = InMemorySession()
    yield session
