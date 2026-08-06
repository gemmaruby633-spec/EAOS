"""Động cơ ghi vết thực thi hệ thống."""

from __future__ import annotations


class TraceEngine:
    """Ghi nhận vết thực thi giao dịch."""

    def __init__(self) -> None:
        self._traces: list[str] = []

    def record_trace(self, trace_id: str) -> None:
        """Ghi vết thực thi."""
        self._traces.append(trace_id)
