"""ISO 27001 and Regulatory Compliance Policy Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CompliancePolicyDTO(BaseModel):
    """Value object representing a Compliance Policy."""

    model_config = ConfigDict(frozen=True)

    standard_name: str = Field(default="ISO27001")
    is_compliant: bool = Field(default=True)
    audit_frequency_days: int = Field(default=90)
