"""Động cơ đánh giá quy tắc Ranh giới Hexagonal."""

from __future__ import annotations

from models import EvaluationResult


class ArchitectureRuleEngine:
    """Kiểm tra tính thuần khiết của Domain Layer."""

    def evaluate_isolation(self, cross_layer_imports: int) -> EvaluationResult:
        """Kiểm tra vi phạm phụ thuộc ngược từ Domain ra ngoài."""
        passed = cross_layer_imports == 0
        msg = (
            "Domain thuần khiết, 0 vi phạm ranh giới."
            if passed
            else f"Phát hiện {cross_layer_imports} vi phạm ranh giới Hexagonal!"
        )
        return EvaluationResult(rule_id="RULE-ARCH-001", passed=passed, message=msg)
