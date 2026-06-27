"""FastAPI application factory and entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import health
from backend.config.settings import Settings, get_settings
from backend.core.logging import configure_logging, get_logger
from backend.core.middleware import RequestLoggingMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown lifecycle."""
    settings: Settings = app.state.settings
    logger.info(
        "application_starting",
        environment=settings.pyrocast_env,
        debug=settings.debug,
    )
    yield
    logger.info("application_shutdown")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings)

    app = FastAPI(
        title="PyroCast API",
        description=(
            "Enterprise wildfire spread prediction platform combining NASA FIRMS, "
            "NOAA HRRR, LANDFIRE terrain data, and Physics-Informed Neural Networks."
        ),
        version="0.1.0",
        docs_url="/docs" if not resolved_settings.is_production else None,
        redoc_url="/redoc" if not resolved_settings.is_production else None,
        lifespan=lifespan,
    )

    app.state.settings = resolved_settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    app.include_router(health.router, tags=["Health"])

    return app


app = create_app()


def run() -> None:
    """CLI entry point for running the API server."""
    settings = get_settings()
    uvicorn.run(
        "backend.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload and settings.is_development,
        workers=settings.api_workers if not settings.api_reload else 1,
        log_config=None,
    )


if __name__ == "__main__":
    run()
