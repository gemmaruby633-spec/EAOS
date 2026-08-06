"""Động cơ kiểm toán DDD Entities."""

from __future__ import annotations


class EntityEngine:
    """Xác minh Entity Identity."""

    def verify_entity(self, entity_name: str) -> bool:
        """Kiểm tra Entity hợp lệ."""
        return len(entity_name) > 0
