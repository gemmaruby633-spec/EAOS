"""Trình biên dịch sơ đồ Mermaid."""

from __future__ import annotations


class MermaidRenderer:
    """Biên dịch JSON Spec sang Mermaid Diagram."""

    @staticmethod
    def to_mermaid(nodes: list[str]) -> str:
        """Sinh mã Mermaid Diagram."""
        lines = ["graph TD"]
        lines.extend(f"  {n}" for n in nodes)
        return "\n".join(lines)
