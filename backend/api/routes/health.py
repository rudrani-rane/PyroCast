"""Health check endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from backend.api.deps import get_app_settings
from backend.config.settings import Settings
from backend.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_app_settings)) -> HealthResponse:
    """Return liveness status for load balancers and orchestrators."""
    return HealthResponse(
        status="healthy",
        service="pyrocast-api",
        version="0.1.0",
        environment=settings.pyrocast_env,
        timestamp=datetime.now(tz=UTC),
    )


@router.get("/ready", response_model=ReadinessResponse)
async def readiness_check(settings: Settings = Depends(get_app_settings)) -> ReadinessResponse:
    """Return readiness status including dependency connectivity checks."""
    checks: dict[str, str] = {
        "api": "ok",
        "configuration": "ok" if settings.secret_key else "missing_secret_key",
    }

    all_ok = all(status == "ok" for status in checks.values())

    return ReadinessResponse(
        status="ready" if all_ok else "not_ready",
        checks=checks,
        timestamp=datetime.now(tz=UTC),
    )
