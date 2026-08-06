"""Động cơ đánh giá quy tắc Chất lượng (Type Safety)."""

from __future__ import annotations

from models import EvaluationResult


class QualityRuleEngine:
    """Kiểm tra tỷ lệ gán kiểu dữ liệu tĩnh MyPy Strict."""

    def evaluate_mypy_strict(self, typed_percentage: float) -> EvaluationResult:
        """Đánh giá tỷ lệ type coverage."""
        passed = typed_percentage >= 100.0
        msg = (
            "Đạt 100% MyPy Strict Type Coverage." if passed else f"Type coverage {typed_percentage:.1f}% chưa đạt 100%!"
        )
        return EvaluationResult(rule_id="RULE-QUAL-001", passed=passed, message=msg)
