"""Application-specific exception hierarchy."""

from typing import Any


class PyroCastError(Exception):
    """Base exception for all PyroCast errors."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(PyroCastError):
    """Raised when application configuration is invalid or incomplete."""


class ExternalServiceError(PyroCastError):
    """Raised when an external data provider returns an error or invalid response."""


class DataValidationError(PyroCastError):
    """Raised when ingested or processed data fails validation."""


class InferenceError(PyroCastError):
    """Raised when ML inference fails."""
