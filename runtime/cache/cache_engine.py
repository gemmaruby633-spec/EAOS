"""Động cơ quản lý bộ nhớ đệm Splay Cache."""

from __future__ import annotations

from typing import Any


class CacheEngine:
    """Động cơ lưu trữ đệm splay cache."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Any | None:
        """Truy xuất dữ liệu đệm."""
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        self._misses += 1
        return None

    def set(self, key: str, value: Any) -> None:
        """Ghi dữ liệu đệm."""
        self._cache[key] = value

    def get_hit_ratio(self) -> float:
        """Tính tỷ lệ truy xuất đệm thành công."""
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 1.0
