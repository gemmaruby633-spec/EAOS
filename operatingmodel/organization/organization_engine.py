"""Organizational Structure and Business Units Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OrgUnitDTO(BaseModel):
    """Value object representing an Organizational Business Unit."""

    model_config = ConfigDict(frozen=True)

    unit_id: str = Field(..., description="Unit ID e.g. org-sales")
    name: str = Field(..., description="Business Unit name")
    head_role: str = Field(default="Chief Officer")


class OrganizationEngine:
    """Engine mapping enterprise organizational structure."""

    def list_business_units(self) -> list[OrgUnitDTO]:
        """Return list of active organizational business units."""
        return [
            OrgUnitDTO(
                unit_id="org-arch",
                name="Architecture Review Board",
                head_role="Chief Architect",
            ),
            OrgUnitDTO(
                unit_id="org-eng",
                name="Engineering Operations",
                head_role="VP of Engineering",
            ),
        ]
