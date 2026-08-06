"""Multi-Agent Swarm Orchestrator Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.agent.domain.swarm_models import (
    SwarmExecutionResult,
)


@runtime_checkable
class SwarmOrchestratorPort(Protocol):
    """Port protocol for orchestrating 5-Agent Swarm pipeline."""

    async def execute_swarm_pipeline(self, goal: str, approval_mode: str = "ASK") -> SwarmExecutionResult: ...
