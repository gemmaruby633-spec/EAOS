"""Động cơ kiểm toán Domain Events."""

from __future__ import annotations


class EventEngine:
    """Xác minh Domain Event payload."""

    def verify_event(self, event_name: str) -> bool:
        """Kiểm tra Event hợp lệ."""
        return event_name.endswith("Event")
