"""API endpoint tests."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient


@pytest.mark.api
class TestHealthEndpoints:
    def test_health_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "healthy"
        assert payload["service"] == "pyrocast-api"
        assert payload["version"] == "0.1.0"
        datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))

    def test_health_includes_request_id_header(self, client: TestClient) -> None:
        response = client.get("/health")
        assert "X-Request-ID" in response.headers

    def test_ready_returns_200(self, client: TestClient) -> None:
        response = client.get("/ready")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] in {"ready", "not_ready"}
        assert "checks" in payload
        assert payload["checks"]["api"] == "ok"

    def test_openapi_schema_available_in_non_production(self, client: TestClient) -> None:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "PyroCast API"
