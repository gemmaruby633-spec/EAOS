"""Động cơ thực thi đặc tả API."""

from __future__ import annotations


class ApiSpecEngine:
    """Kiểm tra tuân thủ API Specs."""

    def verify_api_spec(self, spec_path: str) -> bool:
        """Xác minh đặc tả API."""
        return spec_path.endswith(".md")
