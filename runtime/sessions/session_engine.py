"""Động cơ quản lý phiên làm việc active."""

from __future__ import annotations


class SessionEngine:
    """Quản lý phiên đăng nhập và TTL Token."""

    def __init__(self) -> None:
        self._active_sessions: set[str] = {"sess_admin_01"}

    def get_active_count(self) -> int:
        """Lấy số lượng phiên đang hoạt động."""
        return len(self._active_sessions)
