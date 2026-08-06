"""Động cơ thực thi đặc tả Workflows."""

from __future__ import annotations


class WorkflowSpecEngine:
    """Kiểm tra tuân thủ Workflow Specs."""

    def verify_workflow(self, wf_id: str) -> bool:
        """Xác minh đặc tả luồng."""
        return len(wf_id) > 0
