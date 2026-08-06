"""Mô hình Sáng kiến Chiến lược (Strategic Initiatives)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StrategicObjective:
    """Mục tiêu chiến lược doanh nghiệp (OKR/KRA)."""

    objective_id: str
    name: str
    weight: float


@dataclass
class StrategicInitiative:
    """Sáng kiến kết nối tới các Mục tiêu Chiến lược."""

    initiative_id: str
    name: str
    budget: float
    mapped_objectives: list[StrategicObjective] = field(default_factory=list)

    def calculate_alignment_score(self) -> float:
        """Tính điểm số căn chỉnh chiến lược tổng hợp."""
        return sum(obj.weight for obj in self.mapped_objectives)
