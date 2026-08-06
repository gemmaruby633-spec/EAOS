"""Business Process Architecture Engine (APQC PCF / BPMN)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BusinessProcessDTO(BaseModel):
    """Value object representing a Business Process."""

    model_config = ConfigDict(frozen=True)

    process_id: str = Field(..., description="Process ID e.g. proc-auth")
    name: str = Field(..., description="Process name")
    category: str = Field(default="OPERATIONAL")


class ProcessArchitectureEngine:
    """Engine managing APQC PCF business processes."""

    def list_core_processes(self) -> list[BusinessProcessDTO]:
        """Return core operational business processes."""
        return [
            BusinessProcessDTO(
                process_id="proc-qa-gate",
                name="Zero-Ops Quality Gate Process",
                category="GOVERNANCE",
            )
        ]
