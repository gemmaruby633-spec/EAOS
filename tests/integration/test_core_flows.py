"""Integration tests for EAOS core API flows."""

import uuid

import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """Provide a TestClient instance for the API gateway."""
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    """Verify system gateway health check status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_knowledge_flow(client: TestClient) -> None:
    """Verify knowledge ingestion integration flow."""
    payload = {
        "title": "EAOS Architecture",
        "content": "Modular Monolith",
        "author": "System",
    }
    response = client.post("/knowledge", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "EAOS Architecture"


def test_identity_flow(client: TestClient) -> None:
    """Verify user registration and authentication token issuance."""
    suffix = uuid.uuid4().hex[:8]
    test_email = f"agent.{suffix}@example.com"
    test_username = f"AI_Agent_{suffix}"
    test_password = "SecurePassword123!"

    # 1. Register User / AI Agent
    reg_response = client.post(
        "/users/register",
        json={
            "email": test_email,
            "username": test_username,
            "password": test_password,
        },
    )
    assert reg_response.status_code == 201, (
        f"Registration failed with status {reg_response.status_code}: {reg_response.text}"
    )

    # 2. Login User / AI Agent
    log_response = client.post(
        "/users/login",
        json={
            "email": test_email,
            "password": test_password,
        },
    )
    assert log_response.status_code == 200, f"Login failed with status {log_response.status_code}: {log_response.text}"
    assert "access_token" in log_response.json()
