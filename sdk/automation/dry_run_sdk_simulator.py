"""Mô phỏng cuộc gọi SDK an toàn."""

from __future__ import annotations

from typing import Any


class DryRunSdkSimulator:
    """Mô phỏng cuộc gọi SDK."""

    @staticmethod
    def simulate_call(capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Chạy thử cuộc gọi SDK."""
        return {
            "capability": capability,
            "payload_size": len(payload),
            "status": "SIMULATED_SUCCESS",
        }
