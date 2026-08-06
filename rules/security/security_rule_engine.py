"""Động cơ đánh giá quy tắc An ninh Mật mã."""

from __future__ import annotations

from models import EvaluationResult


class SecurityRuleEngine:
    """Kiểm tra sự hiện diện của Secrets trong mã nguồn."""

    def evaluate_secret_scan(self, secrets_count: int) -> EvaluationResult:
        """Đánh giá vi phạm lộ bí mật."""
        passed = secrets_count == 0
        msg = (
            "0 Secrets tìm thấy trong codebase."
            if passed
            else f"PHÁT HIỆN {secrets_count} SECRETS BỊ LỘ TRONG CODEBASE!"
        )
        return EvaluationResult(rule_id="RULE-SEC-001", passed=passed, message=msg)
