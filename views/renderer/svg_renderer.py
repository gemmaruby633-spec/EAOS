"""Trình biên dịch đồ họa vectơ SVG."""

from __future__ import annotations


class SvgRenderer:
    """Biên dịch JSON Spec sang SVG Vector Graphic."""

    @staticmethod
    def to_svg(title: str) -> str:
        """Sinh mã SVG."""
        return f"<svg><text>{title}</text></svg>"
