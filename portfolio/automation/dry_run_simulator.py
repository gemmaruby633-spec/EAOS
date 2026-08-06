"""Công cụ Mô phỏng Tác động Trước khi Thay đổi (Dry-Run Simulator)."""

from __future__ import annotations

from typing import Any


class DryRunSimulator:
    """Mô phỏng thay đổi cấu trúc/ngân sách mà không ghi nhận thực tế."""

    @staticmethod
    def simulate_budget_reallocation(
        current_allocations: dict[str, float],
        reallocation_delta: dict[str, float],
    ) -> dict[str, Any]:
        """Mô phỏng điều chuyển ngân sách và kiểm tra vi phạm rào chắn."""
        simulated = current_allocations.copy()
        violations: list[str] = []

        for category, delta in reallocation_delta.items():
            new_val = simulated.get(category, 0.0) + delta
            if new_val < 0:
                violations.append(f"Hạng mục {category} bị âm ngân sách ({new_val})")
            simulated[category] = new_val

        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "simulated_allocations": simulated,
        }
