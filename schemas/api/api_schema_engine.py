"""Động cơ xử lý API Schema."""

from __future__ import annotations

from typing import Any


class ApiSchemaEngine:
    """Quản lý đặc tả hợp đồng API."""

    def validate_api_request(self, endpoint: str, data: dict[str, Any]) -> bool:
        """Xác thực cấu trúc yêu cầu API."""
        return len(endpoint) > 0 and isinstance(data, dict)
