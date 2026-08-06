"""Động cơ đánh giá quy tắc Runtime Resilience."""

from __future__ import annotations

from models import EvaluationResult


class RuntimeRuleEngine:
    """Đánh giá ngưỡng ngắt mạch Circuit Breaker."""

    def __init__(self, threshold: float = 0.05) -> None:
        self.threshold = threshold

    def evaluate_circuit_breaker(self, error_rate: float) -> EvaluationResult:
        """Đánh giá tỷ lệ lỗi dịch vụ."""
        passed = error_rate < self.threshold
        msg = (
            f"Tỷ lệ lỗi {error_rate:.3f} ổn định, Circuit CLOSED."
            if passed
            else f"Tỷ lệ lỗi {error_rate:.3f} vượt ngưỡng, Circuit OPEN!"
        )
        return EvaluationResult(rule_id="RULE-RT-001", passed=passed, message=msg)
