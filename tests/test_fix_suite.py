"""Integration tests for EAOS API Gateway Assembly."""

from collections.abc import Generator

import pytest
from apps.api.app.main import app
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> Generator[TestClient]:
    """Provides a TestClient instance for the assembled FastAPI gateway."""
    with TestClient(app) as test_client:
        yield test_client


def test_gateway_dashboard_route_mounted(client: TestClient) -> None:
    """Verifies that the dashboard router is correctly assembled at root level."""
    response = client.get("/dashboard")
    assert response.status_code == status.HTTP_200_OK
    assert "EAOS Cybernetic Control Room" in response.text


def test_gateway_identity_register_route_mounted(client: TestClient) -> None:
    """Verifies that the identity router is mounted under /api/v1 prefix."""
    payload = {
        "email": "arch@eaos.internal",
        "password": "StrongPassword123!",
        "full_name": "EAOS Architect",
    }
    response = client.post("/api/v1/identity/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "arch@eaos.internal"


def test_gateway_unmounted_route_returns_404(client: TestClient) -> None:
    """Verifies that non-existent routes return HTTP 404 appropriately."""
    response = client.get("/api/v1/non-existent-endpoint")
    assert response.status_code == status.HTTP_404_NOT_FOUND