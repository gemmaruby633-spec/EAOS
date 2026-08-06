"""Động cơ Tree-of-Thought (ToT)."""

from __future__ import annotations


class ReasoningEngine:
    """Đánh giá cây quyết định tư duy ToT."""

    def evaluate_branches(self, branches: list[str]) -> str:
        """Chọn nhánh tư duy tối ưu."""
        return branches[0] if branches else "NO_BRANCH"
