"""Comprehensive unit tests for EAOS API Gateway main application module."""

import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """Fixture providing TestClient instance."""
    return TestClient(app)


def test_root_endpoint(client: TestClient) -> None:
    """Verify root endpoint status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"


def test_health_endpoint(client: TestClient) -> None:
    """Verify health diagnostic endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["doctor_score"] == 100


def test_dashboard_endpoint(client: TestClient) -> None:
    """Verify HTML dashboard endpoint."""
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "EAOS Cybernetic Control Room" in response.text


def test_splay_tree_governance_endpoints(client: TestClient) -> None:
    """Verify Splay Tree governance endpoints."""
    res_tree = client.get("/governance/splay-tree")
    assert res_tree.status_code == 200
    assert res_tree.json()["status"] == "ACTIVE"

    res_mermaid = client.get("/governance/splay-tree/mermaid")
    assert res_mermaid.status_code == 200
    assert "mermaid" in res_mermaid.json()


def test_evolution_proposal_and_fitness(client: TestClient) -> None:
    """Verify evolution proposal and fitness evaluation endpoints."""
    payload = {
        "obj_id": "EVO-001",
        "name": "Test Evolution",
        "payload": {"key": "value"},
    }
    res_propose = client.post("/evolution/propose", json=payload)
    assert res_propose.status_code == 201

    res_fitness = client.post("/evolution/evaluate-fitness/EVO-001")
    assert res_fitness.status_code == 200
    assert res_fitness.json()["passed"] is True


def test_reflection_and_learning_flow(client: TestClient) -> None:
    """Verify reflection analysis and learning ingestion endpoints."""
    payload = {
        "subject_id": "SUBJ-001",
        "trigger_event": "TEST_EVENT",
        "passed_checks": True,
    }
    res_reflect = client.post("/reflection/analyze", json=payload)
    assert res_reflect.status_code == 201

    res_learn = client.post(
        "/learning/ingest", json={"reflection_id": "REF-001"}
    )
    assert res_learn.status_code == 201


def test_v1_capabilities_list(client: TestClient) -> None:
    """Verify capabilities v1 listing endpoint."""
    response = client.get("/v1/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2