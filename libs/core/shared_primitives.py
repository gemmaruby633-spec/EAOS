"""Shared Enterprise Core Primitives and DTOs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ResultDTO(BaseModel):
    """Generic Result DTO for operation outcomes."""

    model_config = ConfigDict(frozen=True)

    success: bool = Field(default=True)
    message: str = Field(default="Operation completed successfully.")
    data: dict[str, Any] = Field(default_factory=dict)


class PaginationDTO(BaseModel):
    """Value object representing pagination metadata."""

    model_config = ConfigDict(frozen=True)

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    total_items: int = Field(default=0, ge=0)
