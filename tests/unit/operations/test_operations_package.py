"""Unit tests for operations/ package."""

from __future__ import annotations

from pathlib import Path

from operations.sre.sre_engine import SREEngine
from operations.sre_runbook import EAOSOperationsEngine


def test_sre_engine_health_calculation() -> None:
    """Test calculating SRE availability and error budget."""
    engine = SREEngine()
    metric = engine.calculate_sre_health("api_gateway")

    assert metric.service_name == "api_gateway"
    assert metric.slo_target == 99.9
    assert metric.availability_score == 100.0


def test_operations_engine_summary(tmp_path: Path) -> None:
    """Test master SRE operations engine summary generation."""
    engine = EAOSOperationsEngine(workspace_root=tmp_path)
    summary = engine.get_operations_summary()

    assert summary.sre_availability_score == 100.0
    assert summary.active_incidents_count == 0
    assert summary.runbook_execution_status == "COMPLETED"
