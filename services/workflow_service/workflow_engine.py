"""Động cơ điều phối workflow."""

from __future__ import annotations


class WorkflowEngine:
    """Thực thi luồng công việc."""

    def start_workflow(self, wf_id: str) -> bool:
        """Khởi chạy workflow."""
        return len(wf_id) > 0
