"""Unit tests for engine/ package."""

from __future__ import annotations

from pathlib import Path

from engine.master_engine import EAOSMasterEngine
from engine.planner.task_planner import AutonomousTaskPlannerEngine


def test_autonomous_task_planner(tmp_path: Path) -> None:
    """Test task planning in engine/planner."""
    planner = AutonomousTaskPlannerEngine()
    task = planner.plan_task("Refactor Layer 01", target="kernel")

    assert task.goal == "Refactor Layer 01"
    assert task.target_component == "kernel"
    assert task.task_id.startswith("task-")


def test_master_engine_orchestration(tmp_path: Path) -> None:
    """Test master engine orchestration status."""
    engine = EAOSMasterEngine(workspace_root=tmp_path)
    status = engine.get_engine_status()

    assert status.status == "ACTIVE"
    assert status.sub_engines_count == 12
    assert status.cybernetic_loop_active is True
