"""Động cơ xuất chiếu OS Overview View."""

from __future__ import annotations


class EaosViewEngine:
    """Quản lý View OS Overview."""

    def load_overview_spec(self) -> dict[str, str]:
        """Nạp cấu hình sơ đồ OS Overview."""
        return {"title": "EAOS Overview", "status": "ACTIVE"}
