"""Động cơ kiểm kê tài sản hạ tầng."""

from __future__ import annotations


class InventoryEngine:
    """Quản lý danh mục tài sản hạ tầng đã phát hiện."""

    def __init__(self) -> None:
        self._assets: list[str] = ["server-01", "db-primary"]

    def discover_assets(self) -> list[str]:
        """Trả về danh sách tài sản hạ tầng."""
        return self._assets.copy()
