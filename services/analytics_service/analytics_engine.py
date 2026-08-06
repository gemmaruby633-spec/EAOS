"""Động cơ xử lý Analytics."""

from __future__ import annotations


class AnalyticsEngine:
    """Thu thập telemetry."""

    def record_metric(self, name: str, val: float) -> bool:
        """Ghi nhận chỉ số."""
        return len(name) > 0 and val >= 0
