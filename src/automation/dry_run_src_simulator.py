"""Mô phỏng thay đổi chính sách an toàn."""

from __future__ import annotations

from typing import Any


class DryRunSrcSimulator:
    """Mô phỏng tác động thay đổi quy tắc chính sách."""

    @staticmethod
    def simulate_change(policy_id: str, new_rule_id: str) -> dict[str, Any]:
        """Mô phỏng điều chỉnh chính sách."""
        return {
            "policy_id": policy_id,
            "new_rule_id": new_rule_id,
            "status": "SIMULATION_SUCCESSFUL",
            "impact_risk": "LOW",
        }
