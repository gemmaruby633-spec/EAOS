"""Unit tests verifying upgraded modular architecture of EAOS Web UI."""

from apps.web.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_web_health_endpoint() -> None:
    """Verify primary health endpoint returns expected DTO."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["channel"] == "eaos-web-app"


def test_web_health_detailed_endpoint() -> None:
    """Verify detailed health probe returns settings metadata."""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "settings" in data


def test_custom_exception_handler_json() -> None:
    """Verify 404 error returns JSON error payload for API client."""
    response = client.get("/non-existent-route")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "ERROR"
    assert data["code"] == 404