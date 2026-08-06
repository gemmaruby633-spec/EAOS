"""Interaction Engine Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.interaction_architecture.domain.contracts import (
    InteractionActionDTO,
    InteractionContextDTO,
    InteractionContract,
)


@runtime_checkable
class InteractionEnginePort(Protocol):
    """Port protocol for executing interaction contracts."""

    async def execute_interaction(
        self,
        context: InteractionContextDTO,
        action: InteractionActionDTO,
        payload: str,
    ) -> InteractionContract: ...

    async def verify_evidence(self, evidence_id: str) -> bool: ...
