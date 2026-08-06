"""Động cơ xử lý AI Service."""

from __future__ import annotations


class AiEngine:
    """Động cơ suy luận ai."""

    def predict(self, prompt: str) -> str:
        """Chạy dự đoán ai."""
        return f"AI_RESPONSE_{len(prompt)}"
