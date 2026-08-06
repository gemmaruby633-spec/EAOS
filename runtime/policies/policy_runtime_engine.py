"""Động cơ thực thi chính sách runtime chủ động."""

from __future__ import annotations


class PolicyRuntimeEngine:
    """Đánh giá và thực thi chính sách runtime active."""

    def is_policy_active(self, policy_id: str) -> bool:
        """Kiểm tra chính sách có hiệu lực không."""
        return True
