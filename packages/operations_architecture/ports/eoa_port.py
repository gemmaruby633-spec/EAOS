"""Enterprise Operations Architecture Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.operations_architecture.domain.eoa_models import (
    OpsCapabilityDTO,
    OpsExecutableRunbookDTO,
    OpsRuleDTO,
)


@runtime_checkable
class OperationsArchitecturePort(Protocol):
    """Port protocol for executing and validating EOA rules."""

    async def load_operations_constitution(self) -> list[OpsRuleDTO]: ...

    async def get_capability(self, capability_id: str) -> OpsCapabilityDTO | None: ...

    async def execute_runbook(self, runbook: OpsExecutableRunbookDTO) -> bool: ...
