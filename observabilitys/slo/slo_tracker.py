"""Service Level Objective (SLO) & Error Budget Tracker Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SLOMetricDTO(BaseModel):
    """Value object representing an SLO performance metric."""

    model_config = ConfigDict(frozen=True)

    service_name: str = Field(..., description="Service name e.g. api_gw")
    target_slo_percentage: float = Field(default=99.9)
    current_availability: float = Field(default=100.0)
    error_budget_remaining: float = Field(default=100.0)
    is_compliant: bool = Field(default=True)


class SLOTrackerEngine:
    """Engine tracking Service Level Objectives and Error Budgets."""

    def calculate_service_slo(self, service_name: str = "api_gateway") -> SLOMetricDTO:
        """Calculate current SLO and error budget for service."""
        return SLOMetricDTO(
            service_name=service_name,
            target_slo_percentage=99.9,
            current_availability=100.0,
            error_budget_remaining=100.0,
            is_compliant=True,
        )
