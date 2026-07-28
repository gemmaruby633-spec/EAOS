"""Performance, Concurrency and Splay Eviction Tests."""

from fastapi.testclient import TestClient


def test_concurrency_metrics_and_splay_batch_eviction(client: TestClient) -> None:
    metrics_resp = client.get("/performance/concurrency/metrics")
    assert metrics_resp.status_code == 200
    m_data = metrics_resp.json()
    assert m_data["p99_latency_ms"] < 50.0

    evict_payload = {"target_items": 500}
    evict_resp = client.post("/performance/splay/batch-evict", json=evict_payload)
    assert evict_resp.status_code == 200
    e_data = evict_resp.json()
    assert e_data["status"] == "BATCH_EVICTION_COMPLETED"
