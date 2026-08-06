"""Động cơ xuất chiếu Control Room View."""

from __future__ import annotations


class RuntimeViewEngine:
    """Quản lý View Control Room."""

    def load_control_room_spec(self) -> dict[str, str]:
        """Nạp cấu hình sơ đồ Control Room."""
        return {"title": "Control Room", "mode": "LIVE_DECK"}
