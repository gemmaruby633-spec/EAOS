"""Operational Memory Engine for Incidents and Traces."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OperationalMemoryRecordDTO(BaseModel):
    """Value object representing an operational incident memory."""

    model_config = ConfigDict(frozen=True)

    memory_id: str = Field(..., description="Unique memory ID")
    incident_id: str = Field(..., description="Incident ID")
    root_cause: str = Field(..., description="Root cause summary")
    preventive_rule: str = Field(default="")


class OperationalMemoryEngine:
    """Engine storing operational incident memories."""

    def store_incident_memory(self, incident_id: str, root_cause: str) -> OperationalMemoryRecordDTO:
        """Store an operational incident memory record."""
        return OperationalMemoryRecordDTO(
            memory_id=f"mem-ops-{incident_id.lower()}",
            incident_id=incident_id,
            root_cause=root_cause,
        )
