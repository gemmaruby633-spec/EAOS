"""Động cơ xử lý điểm số rủi ro đe dọa."""

from __future__ import annotations


class ThreatEngine:
    """Tính toán điểm số rủi ro."""

    def calculate_risk_score(self, anomalies_count: int) -> float:
        """Tính điểm rủi ro."""
        return float(anomalies_count * 10)
