"""Động cơ quản trị Sáng kiến Chiến lược."""

from __future__ import annotations

from initiatives.models import StrategicInitiative, StrategicObjective


class InitiativeEngine:
    """Quản lý căn chỉnh Sáng kiến Chiến lược."""

    def __init__(self) -> None:
        self._initiatives: dict[str, StrategicInitiative] = {}

    def create_initiative(
        self,
        initiative_id: str,
        name: str,
        budget: float,
    ) -> StrategicInitiative:
        """Tạo Sáng kiến Chiến lược mới."""
        initiative = StrategicInitiative(
            initiative_id=initiative_id,
            name=name,
            budget=budget,
        )
        self._initiatives[initiative_id] = initiative
        return initiative

    def link_objective(
        self,
        initiative_id: str,
        objective: StrategicObjective,
    ) -> None:
        """Liên kết Mục tiêu Chiến lược vào Sáng kiến."""
        if initiative_id not in self._initiatives:
            raise KeyError(f"Initiative {initiative_id} không tìm thấy.")
        self._initiatives[initiative_id].mapped_objectives.append(objective)
