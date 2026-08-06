"""Unit tests for unified platforms/ package."""

from __future__ import annotations

from pathlib import Path

from platforms.abstraction.platform_abstraction import (
    PlatformAbstractionEngine,
)
from platforms.platform_orchestrator import EAOSPlatformMasterEngine


def test_platform_abstraction_engine() -> None:
    """Test platform hardware abstraction."""
    engine = PlatformAbstractionEngine()
    info = engine.get_platform_info()

    assert info.platform_type == "HYBRID_CLOUD"
    assert info.cpu_cores >= 1


def test_platform_master_engine(tmp_path: Path) -> None:
    """Test master unified platform engine summary."""
    engine = EAOSPlatformMasterEngine(workspace_root=tmp_path)
    summary = engine.get_platform_summary()

    assert summary.status == "ACTIVE"
    assert summary.post_quantum_security_active is True
    assert summary.telemetry_active is True
