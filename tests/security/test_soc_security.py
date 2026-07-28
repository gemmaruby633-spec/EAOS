"""Security and SOC Hardening Integration Tests."""

from fastapi.testclient import TestClient


def test_wazuh_siem_event_streaming_flow(client: TestClient) -> None:
    payload = {
        "tx_id": "TX-SEC-9001",
        "source_ip": "10.0.0.45",
        "action": "SECURITY_VIOLATION_DETECTED",
    }
    response = client.post("/security/wazuh/stream-event", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "STREAMED"


def test_cloudflare_waf_ip_blocking_flow(client: TestClient) -> None:
    payload = {"ip_address": "198.51.100.12"}
    response = client.post("/security/cloudflare/block-ip", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "BLOCKED"


def test_quantum_envelope_encryption_flow(client: TestClient) -> None:
    payload = {
        "secret_data": "postgres://eaos:secret@localhost:5432/eaos",
        "public_key_fingerprint": "kyber768_fp_88291a",
    }
    response = client.post("/security/quantum/encrypt-envelope", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "CRYSTALS-Kyber768" in data["algorithm"]
