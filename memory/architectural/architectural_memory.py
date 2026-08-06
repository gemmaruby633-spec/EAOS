"""Architectural Memory Engine for ADRs and Decision Records."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ArchitecturalMemoryRecordDTO(BaseModel):
    """Value object representing an architectural decision memory."""

    model_config = ConfigDict(frozen=True)

    memory_id: str = Field(..., description="Unique memory ID")
    adr_id: str = Field(..., description="Associated ADR ID")
    decision_summary: str = Field(..., description="Decision summary")
    rationale: str = Field(default="")


class ArchitecturalMemoryEngine:
    """Engine storing and retrieving architectural memory records."""

    def store_adr_memory(self, adr_id: str, decision: str) -> ArchitecturalMemoryRecordDTO:
        """Store an architectural decision memory record."""
        return ArchitecturalMemoryRecordDTO(
            memory_id=f"mem-arch-{adr_id.lower()}",
            adr_id=adr_id,
            decision_summary=decision,
        )
