from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = Field(default="development", alias="DOMPET_ENV")
    version: str = "0.1.0"
    database_url: str = Field(
        default="sqlite:///./dompet.db", alias="DOMPET_DATABASE_URL"
    )

    model_config = {
        "populate_by_name": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
