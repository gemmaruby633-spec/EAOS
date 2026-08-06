"""Động cơ đánh giá quy tắc AI Drift."""

from __future__ import annotations

from models import EvaluationResult


class AiRuleEngine:
    """Kiểm tra độ trôi mô hình AI và độ trễ phản hồi."""

    def __init__(self, max_allowed_drift: float = 0.05) -> None:
        self.max_allowed_drift = max_allowed_drift

    def evaluate_drift(self, current_drift: float) -> EvaluationResult:
        """Đánh giá tỷ lệ trôi AI có vượt ngưỡng cho phép không."""
        passed = current_drift <= self.max_allowed_drift
        msg = (
            f"AI Drift {current_drift:.3f} trong ngưỡng an toàn."
            if passed
            else f"AI Drift {current_drift:.3f} vượt ngưỡng!"
        )
        return EvaluationResult(rule_id="RULE-AI-001", passed=passed, message=msg)
