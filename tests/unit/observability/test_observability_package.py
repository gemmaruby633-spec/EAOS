"""Unit tests for observability/ package."""

from __future__ import annotations

from pathlib import Path

from observabilitys.observability_engine import EAOSObservabilityEngine
from observabilitys.slo.slo_tracker import SLOTrackerEngine


def test_slo_tracker_engine() -> None:
    """Test calculating service SLO and error budget."""
    tracker = SLOTrackerEngine()
    slo = tracker.calculate_service_slo("api_gateway")

    assert slo.service_name == "api_gateway"
    assert slo.target_slo_percentage == 99.9
    assert slo.current_availability == 100.0
    assert slo.is_compliant is True


def test_observability_engine_summary(tmp_path: Path) -> None:
    """Test master observability engine summary generation."""
    engine = EAOSObservabilityEngine(workspace_root=tmp_path)
    summary = engine.get_observability_summary()

    assert summary.prometheus_metrics_active is True
    assert summary.otel_tracing_active is True
    assert summary.slo_status.is_compliant is True
