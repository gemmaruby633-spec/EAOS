"""Assembly Voting and Constitutional Governance Policy Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AssemblyVotingPolicyDTO(BaseModel):
    """Value object representing Assembly Voting Policy."""

    model_config = ConfigDict(frozen=True)

    quorum_percentage: float = Field(default=75.0)
    bft_consensus_required: bool = Field(default=True)
