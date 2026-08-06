"""Động cơ tìm kiếm lai."""

from __future__ import annotations


class SearchEngine:
    """Tìm kiếm vector + BM25."""

    def search(self, query: str) -> list[str]:
        """Thực hiện tìm kiếm."""
        return [f"result_for_{query}"]
