"""Integration tests for Core Baseline Enterprise Flows."""

import uuid
from fastapi.testclient import TestClient


def test_user_registration_flow(client: TestClient) -> None:
    test_email = f"agent.{uuid.uuid4().hex[:6]}@eaos.internal"
    user_resp = client.post(
        "/users/register",
        json={
            "email": test_email,
            "username": "AgentSmith",
            "password": "Password123!",
        },
    )
    assert user_resp.status_code == 201


def test_knowledge_creation_flow(client: TestClient) -> None:
    knw_resp = client.post(
        "/knowledge",
        json={"title": "R1", "content": "Core", "author": "Arch"},
    )
    assert knw_resp.status_code == 201


def test_capability_listing_flow(client: TestClient) -> None:
    cap_resp = client.get("/v1/capabilities")
    assert cap_resp.status_code == 200
