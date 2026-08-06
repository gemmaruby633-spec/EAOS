"""Client SDK thuần Python."""

from __future__ import annotations

from typing import Any


class PythonClient:
    """Client kết nối EAOS API Gateway."""

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def call(self, capability: str, payload: dict[str, Any]) -> dict[str, str]:
        """Thực hiện cuộc gọi API."""
        return {
            "status": "OK",
            "capability": capability,
            "endpoint": self.endpoint,
        }
