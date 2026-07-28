"""Public ports and protocols for Enterprise Capability Packages."""

from typing import Any, Protocol
from packages.capability.domain.models import (
    BusinessCapability,
    CapabilityContext,
    CapabilityExecutionCommandDTO,
    CapabilityExecutionResultDTO,
    CapabilityMetadata,
    DomainEvent,
    EnterpriseCapabilityContext,
)


class CapabilityRegistryPort(Protocol):
    """Full Port interface matching all caller and adapter expectations."""

    def list_all(self) -> list[BusinessCapability]:
        """Lists all active business capabilities."""
        ...

    def find_by_id(self, capability_id: str) -> BusinessCapability | None:
        """Finds capability by ID."""
        ...

    def register(self, capability: Any) -> Any:
        """Registers capability or plugin."""
        ...

    def exists(self, capability_id: str) -> bool:
        """Checks capability existence."""
        ...


class CapabilityProtocol(Protocol):
    """Protocol defining standard interface for all Capability Plugins."""

    @property
    def capability_id(self) -> str:
        """Returns capability ID."""
        ...

    @property
    def version(self) -> str:
        """Returns plugin version."""
        ...

    def supports_action(self, action: str) -> bool:
        """Checks if capability supports action."""
        ...

    def execute(
        self,
        action: str,
        context: EnterpriseCapabilityContext,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Executes capability action within context."""
        ...


__all__ = [
    "BusinessCapability",
    "CapabilityContext",
    "CapabilityExecutionCommandDTO",
    "CapabilityExecutionResultDTO",
    "CapabilityMetadata",
    "CapabilityProtocol",
    "CapabilityRegistryPort",
    "DomainEvent",
]
