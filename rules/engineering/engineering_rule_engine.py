"""Động cơ đánh giá quy tắc Kỹ thuật (Line Length)."""

from __future__ import annotations

from models import EvaluationResult


class EngineeringRuleEngine:
    """Kiểm tra giới hạn dòng mã nguồn < 80 chars."""

    def __init__(self, max_len: int = 79) -> None:
        self.max_len = max_len

    def evaluate_line_length(self, max_found_len: int) -> EvaluationResult:
        """Kiểm tra độ dài dòng code lớn nhất."""
        passed = max_found_len <= self.max_len
        msg = (
            f"Độ dài dòng tối đa {max_found_len} chars đạt chuẩn."
            if passed
            else f"Độ dài dòng {max_found_len} chars vượt giới hạn!"
        )
        return EvaluationResult(rule_id="RULE-ENG-001", passed=passed, message=msg)
