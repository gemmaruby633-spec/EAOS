"""Unit tests for Phase 2: Architecture Review & Planner."""

from __future__ import annotations

from pathlib import Path

import pytest
from packages.business_architecture.adapters.enterprise_planner_adapter import (
    EnterpriseTaskPlannerAdapter,
)
from packages.business_architecture.domain.planner_models import (
    ApprovalMode,
)
from packages.governance.adapters.ast_fitness_adapter import (
    ASTFitnessInspectorAdapter,
)
from packages.solution_architecture.adapters.self_healing_adapter import (
    SelfHealingLoopAdapter,
)


@pytest.mark.anyio
async def test_enterprise_task_planner_approval_modes() -> None:
    """Test task planning and approval modes."""
    adapter = EnterpriseTaskPlannerAdapter()

    plan_auto = await adapter.generate_plan("Refactor CRM", ApprovalMode.AUTO)
    assert plan_auto.approved is True
    assert len(plan_auto.steps) == 3

    plan_ask = await adapter.generate_plan("Refactor CRM", ApprovalMode.ASK)
    assert plan_ask.approved is False
    approved = await adapter.evaluate_approval(plan_ask, ApprovalMode.ASK)
    assert approved is False

    read_only_approved = await adapter.evaluate_approval(plan_ask, ApprovalMode.READ_ONLY)
    assert read_only_approved is False


@pytest.mark.anyio
async def test_ast_fitness_inspector_pure_domain(tmp_path: Path) -> None:
    """Test AST fitness inspection on clean and forbidden imports."""
    adapter = ASTFitnessInspectorAdapter(workspace_root=tmp_path)

    clean_dir = tmp_path / "packages" / "sample" / "domain"
    clean_dir.mkdir(parents=True, exist_ok=True)
    (clean_dir / "clean.py").write_text("class CleanDomain: pass")

    report = await adapter.inspect_repository("packages")
    assert report.score == 100.0
    assert report.passed is True

    forbidden_dir = tmp_path / "packages" / "bad" / "domain"
    forbidden_dir.mkdir(parents=True, exist_ok=True)
    (forbidden_dir / "bad.py").write_text("import fastapi\nclass Bad: pass")

    bad_report = await adapter.inspect_repository("packages")
    assert bad_report.score < 100.0
    assert bad_report.passed is False
    assert len(bad_report.violations) == 1
    assert bad_report.violations[0].rule_id == "R01-DOMAIN-PURITY"


@pytest.mark.anyio
async def test_self_healing_loop_execution(tmp_path: Path) -> None:
    """Test self-healing loop execution."""
    adapter = SelfHealingLoopAdapter(workspace_root=tmp_path)
    res = await adapter.execute_healing_cycle(max_iterations=1)
    assert res.cycle_id.startswith("heal-")
