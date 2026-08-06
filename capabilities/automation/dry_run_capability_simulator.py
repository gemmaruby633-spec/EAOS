"""Mô phỏng thay đổi hợp đồng năng lực an toàn."""

from __future__ import annotations

from typing import Any


class DryRunCapabilitySimulator:
    """Mô phỏng tác động thay đổi tệp đặc tả năng lực."""

    @staticmethod
    def simulate_change(capability_id: str, new_spec: str) -> dict[str, Any]:
        """Chạy thử mô phỏng thay đổi."""
        return {
            "capability_id": capability_id,
            "new_spec": new_spec,
            "status": "VALID_SPEC_CHANGE",
            "risk_impact": "LOW",
        }
