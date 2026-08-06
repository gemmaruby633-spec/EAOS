"""Unit tests for capabilities/ catalog package."""

from __future__ import annotations

from pathlib import Path

from capabilities.capability_registry import CapabilityRegistryEngine


def test_capability_registry_engine_scan(tmp_path: Path) -> None:
    """Test scanning and auditing capabilities catalog."""
    cap_dir = tmp_path / "capabilities" / "sales"
    cap_dir.mkdir(parents=True, exist_ok=True)
    (cap_dir / "api.yaml").write_text("openapi: 3.1.0")
    (cap_dir / "domain.md").write_text("# Sales Domain")

    engine = CapabilityRegistryEngine(workspace_root=tmp_path)
    specs = engine.scan_all_capabilities()

    assert len(specs) == 1
    assert specs[0].capability_id == "sales"
    assert specs[0].has_api_spec is True
    assert specs[0].has_domain_spec is True
