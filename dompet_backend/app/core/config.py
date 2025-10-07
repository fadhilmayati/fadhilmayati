from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    environment: str = os.getenv("DOMPET_ENV", "development")
    version: str = "0.1.0"
    database_url: str = os.getenv("DOMPET_DATABASE_URL", "sqlite:///./dompet.db")
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_anon_key: str | None = os.getenv("SUPABASE_ANON_KEY")
    supabase_jwt_secret: str = os.getenv("SUPABASE_JWT_SECRET", "dev-secret-key")
    supabase_jwt_audience: str | None = os.getenv("SUPABASE_JWT_AUDIENCE")
    posthog_api_key: str | None = os.getenv("POSTHOG_API_KEY")
    posthog_host: str = os.getenv("POSTHOG_HOST", "https://app.posthog.com")
    sentry_dsn: str | None = os.getenv("SENTRY_DSN")
    beta_testers_target: int = int(os.getenv("BETA_TESTERS_TARGET", "20"))
    auth_bypass: bool = os.getenv("DOMPET_AUTH_BYPASS", "false").lower() == "true"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
