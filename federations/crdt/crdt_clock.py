"""Cấu trúc dữ liệu CRDT Vector Clock."""

from __future__ import annotations


class CrdtClock:
    """Quản lý Vector Clock."""

    def increment(self, node_id: str) -> int:
        """Tăng biến đếm clock."""
        return 1
