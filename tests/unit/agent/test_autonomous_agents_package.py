"""Unit tests for agents/ package Workers and Orchestrator."""

from __future__ import annotations

from pathlib import Path

import pytest
from agents.base import AgentRole
from agents.orchestrator import AutonomousAgentSwarm
from agents.planner.worker import PlannerWorker


@pytest.mark.anyio
async def test_planner_worker_execution(tmp_path: Path) -> None:
    """Test PlannerWorker generates plan result."""
    worker = PlannerWorker(workspace_root=tmp_path)
    res = await worker.execute_work("Implement Auth", mode="ASK")

    assert res.agent_role == AgentRole.PLANNER
    assert res.success is True
    assert "Implement Auth" in res.summary


@pytest.mark.anyio
async def test_autonomous_swarm_orchestration(tmp_path: Path) -> None:
    """Test AutonomousAgentSwarm runs 7-agent pipeline."""
    swarm = AutonomousAgentSwarm(workspace_root=tmp_path)
    results = await swarm.run_full_swarm("Optimize RAG", mode="AUTO")

    assert len(results) >= 5
    roles = [r.agent_role for r in results]
    assert AgentRole.PLANNER in roles
    assert AgentRole.ARCHITECT in roles
    assert AgentRole.SECURITY in roles
