"""Mô phỏng chuyển vùng sự cố dịch vụ (Failover Simulator)."""

from __future__ import annotations

from typing import Any


class DryRunRuntimeSimulator:
    """Mô phỏng tác động Failover."""

    @staticmethod
    def simulate_failover(service_id: str) -> dict[str, Any]:
        """Mô phỏng ngắt kết nối dịch vụ."""
        return {
            "service_id": service_id,
            "failover_successful": True,
            "backup_node": "node-secondary-02",
        }
