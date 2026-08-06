"""Unit tests for EAOS Web UI Gateway."""

from apps.web.app.main import app as web_app
from fastapi.testclient import TestClient

client = TestClient(web_app)


def test_web_app_healthcheck() -> None:
    """Verify web UI healthcheck status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["channel"] == "eaos-web-app"


def test_web_app_control_room() -> None:
    """Verify control room page rendering."""
    response = client.get("/control-room")
    assert response.status_code == 200