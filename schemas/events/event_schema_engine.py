"""Động cơ xử lý Domain Event Schema."""

from __future__ import annotations

from typing import Any


class EventSchemaEngine:
    """Quản lý đặc tả sự kiện domain."""

    def validate_event_payload(self, event_name: str, payload: dict[str, Any]) -> bool:
        """Kiểm tra payload sự kiện."""
        return len(event_name) > 0 and "timestamp" in payload
