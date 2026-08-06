"""Enterprise Task Planner Adapter."""

from __future__ import annotations

import uuid

from packages.business_architecture.domain.planner_models import (
    ApprovalMode,
    TaskPlan,
    TaskStep,
)
from packages.business_architecture.ports.planner_port import (
    TaskPlannerPort,
)


class EnterpriseTaskPlannerAdapter(TaskPlannerPort):
    """Adapter decomposing tasks and evaluating approval modes."""

    async def generate_plan(self, goal: str, mode: ApprovalMode) -> TaskPlan:
        plan_id = f"plan-{uuid.uuid4().hex[:8]}"
        steps = [
            TaskStep(
                step_id=1,
                target_file="ARCHITECTURE_CONSTITUTION.md",
                action_type="INSPECT_RULES",
                description="Verify constitutional rules compliance.",
            ),
            TaskStep(
                step_id=2,
                target_file="apps/api/app/routers/control_room.py",
                action_type="GENERATE_PATCH",
                description=f"Generate patch for goal: {goal}",
            ),
            TaskStep(
                step_id=3,
                target_file=("tests/unit/solution/test_phase2_review_planner.py"),
                action_type="VERIFY_TESTS",
                description="Execute verification test suite.",
            ),
        ]

        approved = mode == ApprovalMode.AUTO

        return TaskPlan(
            plan_id=plan_id,
            goal=goal,
            steps=steps,
            mode=mode,
            approved=approved,
        )

    async def evaluate_approval(self, plan: TaskPlan, mode: ApprovalMode) -> bool:
        if mode == ApprovalMode.READ_ONLY:
            return False
        if mode == ApprovalMode.AUTO:
            return True
        return plan.approved
