"""Self-Healing Loop Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.solution_architecture.domain.healing_models import (
    HealingCycleResult,
)


@runtime_checkable
class SelfHealingLoopPort(Protocol):
    """Port protocol for executing auto test and self-healing loop."""

    async def execute_healing_cycle(self, max_iterations: int = 3) -> HealingCycleResult: ...
