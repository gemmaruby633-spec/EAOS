"""Verification tests for master pytest fixtures."""

from fastapi.testclient import TestClient


def test_api_client_fixture_health(api_client: TestClient) -> None:
    """Verifies that api_client yields a functional TestClient for API Gateway."""
    assert isinstance(api_client, TestClient)
    response = api_client.get("/dashboard")
    assert response.status_code == 200


def test_web_client_fixture_health(web_client: TestClient) -> None:
    """Verifies that web_client yields a functional TestClient for Web App."""
    assert isinstance(web_client, TestClient)


def test_client_alias_fixture_health(client: TestClient) -> None:
    """Verifies that the client alias fixture resolves to the API Gateway TestClient."""
    assert isinstance(client, TestClient)
    response = client.get("/dashboard")
    assert response.status_code == 200