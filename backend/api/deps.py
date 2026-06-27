"""FastAPI dependency injection providers."""

from collections.abc import AsyncGenerator

from backend.config.settings import Settings, get_settings


def get_app_settings() -> Settings:
    """Provide application settings to route handlers."""
    return get_settings()


async def get_db_session() -> AsyncGenerator[None, None]:
    """Database session dependency (implemented in Phase 2)."""
    yield None
