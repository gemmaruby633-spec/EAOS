"""Mô phỏng thay đổi ngưỡng quy tắc an toàn."""

from __future__ import annotations

from typing import Any


class DryRunRuleSimulator:
    """Đánh giá tác động trước khi thay đổi ngưỡng chính sách."""

    @staticmethod
    def simulate_threshold_change(
        rule_id: str,
        current_threshold: float,
        proposed_threshold: float,
    ) -> dict[str, Any]:
        """Mô phỏng điều chỉnh ngưỡng."""
        delta = proposed_threshold - current_threshold
        is_stricter = delta < 0
        return {
            "rule_id": rule_id,
            "current": current_threshold,
            "proposed": proposed_threshold,
            "is_stricter": is_stricter,
            "risk_impact": "HIGH" if is_stricter else "LOW",
        }
