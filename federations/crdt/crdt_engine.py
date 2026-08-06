"""Động cơ giải quyết xung đột CRDT."""

from __future__ import annotations


class CrdtEngine:
    """Hợp nhập hai Vector Clocks."""

    def merge_clocks(self, clock_a: dict[str, int], clock_b: dict[str, int]) -> dict[str, int]:
        """Gộp trạng thái clock."""
        res = clock_a.copy()
        for k, v in clock_b.items():
            res[k] = max(res.get(k, 0), v)
        return res
