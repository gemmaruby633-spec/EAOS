"""Zero-Ops Quality Gates Policy Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class QualityGatesPolicyDTO(BaseModel):
    """Value object representing Zero-Ops Quality Gates Policy."""

    model_config = ConfigDict(frozen=True)

    zero_errors_required: bool = Field(default=True)
    min_coverage_percentage: float = Field(default=80.0)
