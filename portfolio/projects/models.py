"""Mô hình Quản lý Dự án và Chỉ số EVM (Earned Value Management)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EarnedValueMetrics:
    """Chỉ số quản lý giá trị thu được (EVM)."""

    planned_value: float
    actual_cost: float
    earned_value: float

    @property
    def cpi(self) -> float:
        """Cost Performance Index (EV / AC)."""
        if self.actual_cost <= 0:
            return 1.0
        return self.earned_value / self.actual_cost

    @property
    def spi(self) -> float:
        """Schedule Performance Index (EV / PV)."""
        if self.planned_value <= 0:
            return 1.0
        return self.earned_value / self.planned_value

    def estimate_at_completion(self, bac: float) -> float:
        """Estimate At Completion (EAC = BAC / CPI)."""
        current_cpi = self.cpi
        if current_cpi <= 0:
            return bac
        return bac / current_cpi


@dataclass
class PortfolioProject:
    """Mô hình Dự án Thực thi."""

    project_id: str
    name: str
    budget_at_completion: float
    evm: EarnedValueMetrics
