"""Enterprise Task Planner Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.business_architecture.domain.planner_models import (
    ApprovalMode,
    TaskPlan,
)


@runtime_checkable
class TaskPlannerPort(Protocol):
    """Port protocol for enterprise task planning and approval."""

    async def generate_plan(self, goal: str, mode: ApprovalMode) -> TaskPlan: ...

    async def evaluate_approval(self, plan: TaskPlan, mode: ApprovalMode) -> bool: ...
