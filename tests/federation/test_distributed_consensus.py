"""Distributed Federation and Consensus Tests (CRDT, Synod, Raft)."""

from fastapi.testclient import TestClient


def test_crdt_cross_region_sync(client: TestClient) -> None:
    payload = {
        "delta": {
            "node_id": "node-us-east-1",
            "region": "us-east-1",
            "vector_clock": {"node-us-east-1": 1},
            "payload": {"status": "ACTIVE"},
        }
    }
    response = client.post("/federation/crdt/sync-delta", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["synced"] is True


def test_bft_synod_federation(client: TestClient) -> None:
    payload = {
        "proposal_id": "prop_9001",
        "action": "FEDERATION_CROSS_BORDER_SYNC",
        "votes": [
            {"node": "node_1", "decision": "APPROVE"},
            {"node": "node_2", "decision": "APPROVE"},
            {"node": "node_3", "decision": "APPROVE"},
            {"node": "node_4", "decision": "REJECT"},
        ],
    }
    response = client.post("/federation/synod/vote-bft", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["achieved_bft_consensus"] is True
