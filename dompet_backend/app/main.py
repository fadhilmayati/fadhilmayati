from fastapi import FastAPI

from .api import ingestion, insights
from .core.config import settings
from .services.database import init_db

app = FastAPI(
    title="Dompet Backend",
    description="API for Dompet personal finance copilot",
    version=settings.version,
)


@app.on_event("startup")
def on_startup() -> None:  # pragma: no cover - framework hook
    init_db()


app.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
app.include_router(insights.router, prefix="/insights", tags=["insights"])


@app.get("/health", tags=["meta"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
