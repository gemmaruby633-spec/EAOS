"""Operating Roles and RACI Matrix Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OperatingRoleDTO(BaseModel):
    """Value object representing an Operating Role in EAOS."""

    model_config = ConfigDict(frozen=True)

    role_id: str = Field(..., description="Role ID e.g. role-ca")
    title: str = Field(..., description="Role title")
    raci_responsibilities: list[str] = Field(default_factory=list)


class RoleMatrixEngine:
    """Engine managing operating roles and RACI matrix."""

    def list_operating_roles(self) -> list[OperatingRoleDTO]:
        """Return list of operating roles in EAOS."""
        return [
            OperatingRoleDTO(
                role_id="role-ca",
                title="Chief Enterprise Architect",
                raci_responsibilities=["Accountable for Architecture"],
            )
        ]
