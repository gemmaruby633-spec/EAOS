"""Quy tắc kiểm tra vi dịch vụ."""

from __future__ import annotations


def is_valid_endpoint(endpoint: str) -> bool:
    """Kiểm tra đường dẫn endpoint."""
    return endpoint.startswith("/")
