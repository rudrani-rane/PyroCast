"""Integration tests for structured logging."""

import logging

import pytest

from backend.config.settings import Settings
from backend.core.logging import configure_logging, get_logger


@pytest.mark.integration
class TestLogging:
    def test_configure_logging_json(self, test_settings: Settings) -> None:
        json_settings = test_settings.model_copy(update={"log_format": "json"})
        configure_logging(json_settings)
        logger = get_logger("test")
        assert hasattr(logger, "info")
        assert hasattr(logger, "bind")

    def test_configure_logging_console(self, test_settings: Settings) -> None:
        console_settings = test_settings.model_copy(update={"log_format": "console"})
        configure_logging(console_settings)
        root = logging.getLogger()
        assert root.level == getattr(logging, console_settings.log_level)
