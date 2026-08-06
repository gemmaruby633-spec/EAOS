"""Mô phỏng chuyển vùng sự cố vi dịch vụ an toàn."""

from __future__ import annotations

from typing import Any


class DryRunServiceSimulator:
    """Mô phỏng thử nghiệm Failover."""

    @staticmethod
    def simulate_failover(service_id: str) -> dict[str, Any]:
        """Mô phỏng sự cố ngắt dịch vụ."""
        return {
            "service_id": service_id,
            "failover_status": "SUCCESSFUL",
            "failover_target": "node-secondary-01",
        }
