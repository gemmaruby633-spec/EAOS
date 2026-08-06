"""Unit tests for contracts/ package."""

from __future__ import annotations

from pathlib import Path

from contracts.contract_registry import EnterpriseContractRegistryEngine


def test_contract_registry_engine_audit(tmp_path: Path) -> None:
    """Test auditing API and protocol contracts."""
    rest_dir = tmp_path / "contracts" / "rest"
    rest_dir.mkdir(parents=True, exist_ok=True)
    (rest_dir / "openapi_gateway_spec.json").write_text('{"openapi": "3.1.0"}')

    engine = EnterpriseContractRegistryEngine(workspace_root=tmp_path)
    contracts = engine.audit_all_contracts()

    assert len(contracts) >= 5
    protocols = [c.protocol for c in contracts]
    assert "REST" in protocols
    assert "GRPC" in protocols
    assert "GRAPHQL" in protocols
    assert "MCP" in protocols
    assert "EVENT" in protocols
