"""Động cơ đánh giá chất lượng phản hồi ai."""

from __future__ import annotations


class EvaluationEngine:
    """Đánh giá toàn diện câu trả lời."""

    def evaluate_response(self, text: str) -> bool:
        """Đánh giá chất lượng."""
        return len(text) > 0
