"""Động cơ lập kế hoạch ai."""

from __future__ import annotations


class PlannerEngine:
    """Sắp xếp thứ tự thực thi task."""

    def build_plan(self, tasks: list[str]) -> list[str]:
        """Xây dựng kế hoạch thực thi."""
        return sorted(tasks)
