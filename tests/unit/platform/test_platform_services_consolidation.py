"""Unit tests for consolidated platforms/ package."""

from __future__ import annotations

from pathlib import Path

from platforms.master_platform_engine import (
    EAOSMasterPlatformEngine,
)
from platforms.platform_abstraction import (
    UnifiedPlatformAbstractionEngine,
)


def test_platform_abstraction_engine() -> None:
    """Test unified platform abstraction status."""
    engine = UnifiedPlatformAbstractionEngine()
    status = engine.get_platform_abstraction_status()

    assert status.is_consolidated is True
    assert status.platform_id == "platform-unified"


def test_master_platform_engine_summary(tmp_path: Path) -> None:
    """Test master platform engine summary generation."""
    engine = EAOSMasterPlatformEngine(workspace_root=tmp_path)
    summary = engine.get_platform_summary()

    assert summary.platform_status == "CONSOLIDATED_ACTIVE"
    assert summary.total_services_count == 13
    assert summary.post_quantum_security_active is True
