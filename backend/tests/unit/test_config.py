"""Unit tests for application configuration."""

import pytest

from backend.config.settings import Settings


@pytest.mark.unit
class TestSettings:
    def test_default_environment(self, test_settings: Settings) -> None:
        assert test_settings.pyrocast_env == "test"

    def test_cors_origins_parsed_from_string(self) -> None:
        settings = Settings(
            secret_key="test-secret-key-for-pytest-minimum-32-chars",
            cors_origins="http://a.com, http://b.com",
        )
        assert settings.cors_origin_list == ["http://a.com", "http://b.com"]

    def test_prediction_horizon_bounds(self) -> None:
        settings = Settings(
            secret_key="test-secret-key-for-pytest-minimum-32-chars",
            prediction_horizon_hours=24,
        )
        assert settings.prediction_horizon_hours == 24

    def test_is_test_flag(self, test_settings: Settings) -> None:
        assert test_settings.is_test is True
        assert test_settings.is_production is False
