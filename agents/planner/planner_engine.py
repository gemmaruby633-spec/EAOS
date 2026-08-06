"""Động cơ lập kế hoạch của Planner Agent."""

from __future__ import annotations


class PlannerEngine:
    """Lập kế hoạch DAG Task."""

    def plan_sprint(self, goal: str) -> list[str]:
        """Phân rã mục tiêu thành danh sách tasks."""
        return [f"task_for_{goal}"]
