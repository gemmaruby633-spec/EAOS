"""Data Lineage and Pipeline Tracking Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DataLineageEdgeDTO(BaseModel):
    """Value object representing data flow between nodes."""

    model_config = ConfigDict(frozen=True)

    source_node: str = Field(..., description="Source dataset")
    target_node: str = Field(..., description="Target dataset")
    transformation: str = Field(default="ETL_SYNC")


class DataLineageEngine:
    """Engine tracking enterprise data flow lineage."""

    def trace_lineage(self, capability_id: str) -> list[DataLineageEdgeDTO]:
        """Return data lineage edges for capability."""
        return [
            DataLineageEdgeDTO(
                source_node=f"raw_{capability_id}_events",
                target_node=f"processed_{capability_id}_lake",
                transformation="KAIZEN_DISTILLATION",
            )
        ]
