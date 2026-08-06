"""Unit tests for operatingmodel/ package."""

from __future__ import annotations

from pathlib import Path

from operatingmodel.model_registry import OperatingModelRegistryEngine
from operatingmodel.value_streams.value_stream_engine import (
    ValueStreamEngine,
)


def test_value_stream_engine() -> None:
    """Test lead-to-cash value stream retrieval."""
    engine = ValueStreamEngine()
    vs = engine.get_lead_to_cash_stream()

    assert vs.stream_id == "vs-lead-to-cash"
    assert len(vs.stages) == 2
    assert vs.stages[0].stage_id == "stg-01"


def test_operating_model_registry_summary(tmp_path: Path) -> None:
    """Test master operating model summary generation."""
    registry = OperatingModelRegistryEngine(workspace_root=tmp_path)
    summary = registry.get_operating_model_summary()

    assert summary.total_value_streams == 1
    assert summary.total_org_units >= 2
    assert summary.total_processes >= 1
    assert summary.total_roles >= 1
    assert summary.total_services >= 1
    assert summary.value_stream.stream_id == "vs-lead-to-cash"
