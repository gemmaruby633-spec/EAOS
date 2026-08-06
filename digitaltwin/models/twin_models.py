"""Digital Twin State Models for Enterprise Simulation."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class ComponentTwinStateDTO(BaseModel):
    """State representation of a single enterprise component."""

    model_config = ConfigDict(frozen=True)

    component_id: str = Field(..., description="Component ID e.g. api_gw")
    component_name: str = Field(..., description="Canonical name")
    health_score: float = Field(default=100.0)
    latency_ms: float = Field(default=5.0)
    is_active: bool = Field(default=True)


class EnterpriseTwinStateDTO(BaseModel):
    """Aggregate state representation of the Enterprise Digital Twin."""

    model_config = ConfigDict(frozen=True)

    twin_id: str = Field(..., description="Unique Digital Twin ID")
    overall_health_score: float = Field(default=100.0)
    active_components_count: int = Field(default=0)
    components: list[ComponentTwinStateDTO] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
