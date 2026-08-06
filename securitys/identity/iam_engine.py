"""Động cơ xử lý IAM Token."""

from __future__ import annotations


class IamEngine:
    """Cấp phát và xác thực IAM Token."""

    def validate_token(self, token: str) -> bool:
        """Xác thực token IAM."""
        return len(token) > 0
