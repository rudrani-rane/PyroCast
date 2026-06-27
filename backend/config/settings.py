"""Pydantic settings for PyroCast application configuration."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration object sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    pyrocast_env: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = False
    secret_key: str = Field(min_length=32)
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    api_reload: bool = False

    # CORS (comma-separated string in .env)
    cors_origins: str = "http://localhost:3000"

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: Literal["json", "console"] = "json"

    # Database
    postgres_user: str = "pyrocast"
    postgres_password: str = "pyrocast"
    postgres_db: str = "pyrocast"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    database_url: PostgresDsn | str = Field(
        default="postgresql+asyncpg://pyrocast:pyrocast@localhost:5432/pyrocast"
    )

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_url: RedisDsn | str = Field(default="redis://localhost:6379/0")

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    celery_task_always_eager: bool = False

    # External APIs
    nasa_firms_api_key: str = ""
    nasa_firms_base_url: str = "https://firms.modaps.eosdis.nasa.gov/api"

    # ML / Inference
    model_checkpoint_path: str = "models/checkpoints"
    inference_device: Literal["cpu", "cuda", "mps"] = "cpu"
    prediction_horizon_hours: int = Field(default=24, ge=12, le=48)
    raster_resolution_meters: int = Field(default=30, ge=10, le=100)

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_development(self) -> bool:
        return self.pyrocast_env == "development"

    @property
    def is_production(self) -> bool:
        return self.pyrocast_env == "production"

    @property
    def is_test(self) -> bool:
        return self.pyrocast_env == "test"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
