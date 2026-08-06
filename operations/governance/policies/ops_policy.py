"""Ops Policy Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class OpsPolicyDTO(BaseModel):
    """DTO for Ops Policy."""

    model_config = ConfigDict(frozen=True)

    policy_id: str = "POL-OPS-01"
