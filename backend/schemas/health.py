"""Health check response schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Liveness probe response."""

    status: Literal["healthy", "unhealthy"]
    service: str
    version: str
    environment: str
    timestamp: datetime = Field(description="UTC timestamp of the health check")


class ReadinessResponse(BaseModel):
    """Readiness probe response with dependency status."""

    status: Literal["ready", "not_ready"]
    checks: dict[str, str]
    timestamp: datetime = Field(description="UTC timestamp of the readiness check")
