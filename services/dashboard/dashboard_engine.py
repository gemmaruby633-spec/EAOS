"""Động cơ Dashboard UI."""

from __future__ import annotations


class DashboardEngine:
    """Backend dữ liệu Dashboard."""

    def get_stats(self) -> dict[str, str]:
        """Lấy thống kê hệ thống."""
        return {"status": "HEALTHY", "active_nodes": "10"}
