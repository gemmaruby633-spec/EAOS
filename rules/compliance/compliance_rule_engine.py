"""Động cơ đánh giá quy tắc Tuân thủ Pháp lý (GDPR)."""

from __future__ import annotations

from models import EvaluationResult


class ComplianceRuleEngine:
    """Kiểm tra thời gian lưu trữ dữ liệu cá nhân (GDPR)."""

    def __init__(self, max_days: int = 365) -> None:
        self.max_days = max_days

    def evaluate_gdpr_retention(self, days_stored: int) -> EvaluationResult:
        """Đánh giá thời hạn lưu trữ PII."""
        passed = days_stored <= self.max_days
        msg = (
            f"Thời gian lưu trữ {days_stored} ngày tuân thủ GDPR."
            if passed
            else f"Dữ liệu {days_stored} ngày vượt thời hạn!"
        )
        return EvaluationResult(rule_id="RULE-CMP-001", passed=passed, message=msg)
