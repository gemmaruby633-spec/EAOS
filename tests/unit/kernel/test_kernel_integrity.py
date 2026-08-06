"""Unit tests for kernel/ package."""

from __future__ import annotations

from pathlib import Path

from kernel.kernel_orchestrator import EAOSKernelOrchestrator
from kernel.policies.kernel_policies import KernelPolicyEngine


def test_kernel_policy_engine_invariants() -> None:
    """Test retrieving frozen kernel policy invariants."""
    engine = KernelPolicyEngine()
    invariants = engine.get_kernel_invariants()

    assert len(invariants) >= 2
    assert invariants[0].policy_id == "POL-K01"
    assert invariants[0].is_enforced is True


def test_kernel_orchestrator_integrity_audit(tmp_path: Path) -> None:
    """Test auditing frozen core kernel integrity."""
    orchestrator = EAOSKernelOrchestrator(workspace_root=tmp_path)
    status = orchestrator.audit_kernel_integrity()

    assert status.status == "FROZEN_SECURE"
    assert status.has_zero_external_dependencies is True
    assert status.invariants_enforced_count >= 2
