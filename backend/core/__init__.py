"""Core application infrastructure: logging, middleware, lifecycle."""

from backend.core.logging import configure_logging, get_logger

__all__ = ["configure_logging", "get_logger"]
