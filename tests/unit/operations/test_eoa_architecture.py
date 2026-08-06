"""Unit test suite for Enterprise Operations Architecture (EOA)."""

from __future__ import annotations

from pathlib import Path

import pytest
from packages.operations_architecture.adapters.eoa_engine_adapter import (
    EOAEngineAdapter,
)
from packages.operations_architecture.domain.eoa_models import (
    OpsExecutableRunbookDTO,
)


@pytest.mark.anyio
async def test_eoa_constitution_and_capability_loading(
    tmp_path: Path,
) -> None:
    """Test loading EOA Constitution rules and capability metadata."""
    adapter = EOAEngineAdapter(workspace_root=tmp_path)
    rules = await adapter.load_operations_constitution()

    assert len(rules) == 5
    assert rules[0].rule_id == "OPS-001"
    assert rules[0].severity == "CRITICAL"

    cap = await adapter.get_capability("OPS-CAP-001")
    assert cap is not None
    assert cap.capability_id == "OPS-CAP-001"
    assert cap.slo_target == "99.99%"


@pytest.mark.anyio
async def test_eoa_executable_runbook_execution(tmp_path: Path) -> None:
    """Test EOA Layer 7 declarative runbook execution."""
    adapter = EOAEngineAdapter(workspace_root=tmp_path)
    runbook = OpsExecutableRunbookDTO(
        runbook_id="RB-BACKUP-01",
        capability_id="OPS-CAP-001",
        steps=[{"step": 1, "action": "verify_storage"}],
        automated=True,
    )

    success = await adapter.execute_runbook(runbook)
    assert success is True
