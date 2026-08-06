"""Unit tests for Phase 4: Multi-Agent Swarm Orchestration."""

from __future__ import annotations

import pytest
from packages.agent.adapters.swarm_orchestrator_adapter import (
    SequentialSwarmOrchestratorAdapter,
)
from packages.agent.domain.swarm_models import AgentRole


@pytest.mark.anyio
async def test_swarm_orchestrator_pipeline_execution() -> None:
    """Verify 5-Agent Swarm pipeline sequential execution."""
    adapter = SequentialSwarmOrchestratorAdapter()
    res = await adapter.execute_swarm_pipeline(
        goal="Implement Content Monetization Capability",
        approval_mode="ASK",
    )

    assert res.success is True
    assert res.completed_agents == 5
    assert len(res.step_results) == 5

    roles = [step.role for step in res.step_results]
    assert roles == [
        AgentRole.PLANNER,
        AgentRole.ARCHITECT,
        AgentRole.CODER,
        AgentRole.REVIEWER,
        AgentRole.TESTER,
    ]
