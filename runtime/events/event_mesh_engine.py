"""Động cơ Event Mesh Queue hỗ trợ NDJSON."""

from __future__ import annotations

import json


class EventMeshEngine:
    """Động cơ đẩy và đọc sự kiện hệ thống."""

    def __init__(self) -> None:
        self._queue: list[dict[str, str]] = []

    def publish_event(self, event_type: str, payload: str) -> str:
        """Bắn sự kiện vào Event Mesh."""
        event = {"type": event_type, "payload": payload}
        self._queue.append(event)
        return json.dumps(event)
