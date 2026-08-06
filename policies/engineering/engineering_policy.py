"""Clean Code and Line Length Engineering Policy Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EngineeringPolicyDTO(BaseModel):
    """Value object representing an Engineering Quality Policy."""

    model_config = ConfigDict(frozen=True)

    max_line_length: int = Field(default=80)
    type_hints_required: bool = Field(default=True)
    strict_mypy_enabled: bool = Field(default=True)
