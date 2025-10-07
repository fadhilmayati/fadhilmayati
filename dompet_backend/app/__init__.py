"""Package exports for the Dompet FastAPI application."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - import only for type checking
    from .main import app as _app

__all__ = ["app"]


def __getattr__(name: str) -> Any:
    """Lazily import the FastAPI app to avoid runtime dependencies in tests."""

    if name == "app":
        from .main import app as _app  # Local import to defer FastAPI dependency

        return _app
    raise AttributeError(name)
