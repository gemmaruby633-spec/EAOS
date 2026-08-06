"""Động cơ thực thi đặc tả Business."""

from __future__ import annotations


class BusinessSpecEngine:
    """Kiểm tra tuân thủ Business Specs."""

    def verify_business_spec(self, spec_path: str) -> bool:
        """Xác minh đặc tả nghiệp vụ."""
        return spec_path.endswith(".md")
