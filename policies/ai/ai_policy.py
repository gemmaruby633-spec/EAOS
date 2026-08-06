"""AI Governance Policy Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AIPolicyDTO(BaseModel):
    """Value object representing an AI Governance Policy."""

    model_config = ConfigDict(frozen=True)

    policy_id: str = Field(..., description="Policy ID e.g. POL-AI-01")
    max_prompt_tokens: int = Field(default=65536)
    hallucination_guard_enabled: bool = Field(default=True)
