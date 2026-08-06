"""Unit tests for policies/ package."""

from __future__ import annotations

from pathlib import Path

from policies.engineering.engineering_policy import EngineeringPolicyDTO
from policies.policy_manifest_loader import PolicyManifestLoaderEngine


def test_engineering_policy_defaults() -> None:
    """Test engineering policy PEP 8 line length limit."""
    policy = EngineeringPolicyDTO()
    assert policy.max_line_length == 80
    assert policy.strict_mypy_enabled is True


def test_policy_manifest_loader_audit(tmp_path: Path) -> None:
    """Test policy manifest loader engine audit."""
    pol_dir = tmp_path / "policies" / "quality"
    pol_dir.mkdir(parents=True, exist_ok=True)
    (pol_dir / "quality_gates_policy.yaml").write_text("policy: quality")

    loader = PolicyManifestLoaderEngine(workspace_root=tmp_path)
    summary = loader.audit_all_policies()

    assert summary.total_yaml_policies >= 1
    assert summary.all_enforced is True
