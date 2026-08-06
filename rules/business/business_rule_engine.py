"""Động cơ đánh giá quy tắc Kinh doanh."""

from __future__ import annotations

from models import EvaluationResult


class BusinessRuleEngine:
    """Đánh giá hạn mức và giá trị giao dịch kinh doanh."""

    def __init__(self, min_order_val: float = 100.0) -> None:
        self.min_order_val = min_order_val

    def evaluate_order_value(self, value: float) -> EvaluationResult:
        """Kiểm tra giá trị đơn hàng tối thiểu."""
        passed = value >= self.min_order_val
        msg = "Đơn hàng  đạt hạn mức tối thiểu." if passed else "Đơn hàng  thấp hơn hạn mức!"
        return EvaluationResult(rule_id="RULE-BIZ-001", passed=passed, message=msg)
