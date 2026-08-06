"""Động cơ xác thực Identity."""

from __future__ import annotations


class IdentityEngine:
    """Xác thực người dùng."""

    def authenticate(self, user_id: str) -> bool:
        """Xác thực định danh."""
        return len(user_id) > 0
