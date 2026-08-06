"""Động cơ tối ưu hóa Prompt."""

from __future__ import annotations


class PromptEngine:
    """Tự động viết lại Prompt (Self-Rewrite)."""

    def optimize_prompt(self, raw_prompt: str) -> str:
        """Tối ưu hóa prompt."""
        return f"System: Optimized\nUser: {raw_prompt}"
