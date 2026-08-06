"""Động cơ định tuyến API Gateway."""

from __future__ import annotations


class GatewayRouter:
    """Định tuyến cuộc gọi API."""

    def route_request(self, path: str) -> str:
        """Định tuyến đường dẫn."""
        return f"ROUTED_TO_{path.strip('/')}"
