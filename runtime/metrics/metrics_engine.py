"""Động cơ thu thập chỉ số Prometheus Realtime."""

from __future__ import annotations


class MetricsEngine:
    """Động cơ quản lý chỉ số Prometheus."""

    def __init__(self) -> None:
        self._counters: dict[str, float] = {}

    def increment_counter(self, metric_name: str, value: float = 1.0) -> None:
        """Tăng biến đếm chỉ số."""
        self._counters[metric_name] = self._counters.get(metric_name, 0.0) + value
