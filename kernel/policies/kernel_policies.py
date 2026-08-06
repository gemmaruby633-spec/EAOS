"""Kernel Constitutional Invariants and Policy Guardrails."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class KernelPolicyInvariantDTO(BaseModel):
    """Value object representing a Frozen Kernel Policy Invariant."""

    model_config = ConfigDict(frozen=True)

    policy_id: str = Field(..., description="Policy ID e.g. POL-K01")
    statement: str = Field(..., description="Invariant statement")
    is_enforced: bool = Field(default=True)


class KernelPolicyEngine:
    """Engine enforcing frozen core constitutional invariants."""

    def get_kernel_invariants(self) -> list[KernelPolicyInvariantDTO]:
        """Return mandatory frozen kernel policy invariants."""
        return [
            KernelPolicyInvariantDTO(
                policy_id="POL-K01",
                statement="Core Kernel shall remain zero-dependency.",
            ),
            KernelPolicyInvariantDTO(
                policy_id="POL-K02",
                statement="Domain logic shall not import external frameworks.",
            ),
        ]
