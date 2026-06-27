"""Shared pytest fixtures and configuration."""

import os
from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Set test environment before importing application modules.
os.environ.setdefault("PYROCAST_ENV", "test")
os.environ.setdefault(
    "SECRET_KEY",
    "test-secret-key-for-pytest-minimum-32-chars",
)
os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "true")
os.environ.setdefault("LOG_FORMAT", "console")

from backend.api.main import create_app
from backend.config.settings import Settings, get_settings


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Provide test-scoped application settings."""
    get_settings.cache_clear()
    return get_settings()


@pytest.fixture
def app(test_settings: Settings) -> Generator[FastAPI, None, None]:
    """Provide a fresh FastAPI application instance."""
    get_settings.cache_clear()
    application = create_app(test_settings)
    yield application
    get_settings.cache_clear()


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    """Provide a synchronous HTTP test client."""
    with TestClient(app) as test_client:
        yield test_client
