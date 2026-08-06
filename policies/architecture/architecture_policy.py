"""Architecture Rules and Retention Policy Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ArchitecturePolicyDTO(BaseModel):
    """Value object representing an Architecture Policy."""

    model_config = ConfigDict(frozen=True)

    policy_id: str = Field(..., description="Policy ID e.g. P-001")
    retention_days: int = Field(default=30)
    compaction_enabled: bool = Field(default=True)
