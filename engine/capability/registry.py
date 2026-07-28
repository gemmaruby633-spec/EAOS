"""Enterprise Capability Registry Facade maintaining 100% API contract."""

import logging
from typing import Any, Protocol, overload
from packages.capability.domain.models import (
    BusinessCapability,
    CapabilityMetadata,
    EnterpriseCapabilityContext,
)

logger = logging.getLogger(__name__)


class CapabilityPluginProtocol(Protocol):
    """Protocol defining interface for pluggable capability modules."""

    @property
    def capability_id(self) -> str: ...

    @property
    def version(self) -> str: ...

    def supports_action(self, action: str) -> bool: ...

    def execute(
        self,
        action: str,
        context: EnterpriseCapabilityContext,
        payload: dict[str, Any],
    ) -> dict[str, Any]: ...


class EnterpriseCapabilityRegistry:
    """Registry Facade implementing full public API for legacy & runtime."""

    def __init__(self) -> None:
        self._plugins: dict[str, Any] = {}
        self._enabled: dict[str, bool] = {}

    @overload
    def register(self, plugin: BusinessCapability) -> BusinessCapability: ...

    @overload
    def register(self, plugin: CapabilityPluginProtocol) -> CapabilityPluginProtocol: ...

    @overload
    def register(self, plugin: Any) -> Any: ...

    def register(self, plugin: Any) -> Any:
        """Registers a capability plugin or BusinessCapability."""
        cap_id = getattr(
            plugin,
            "capability_id",
            getattr(plugin, "id", str(plugin)),
        ).lower()
        self._plugins[cap_id] = plugin
        self._enabled[cap_id] = True
        logger.info("Registered Capability: %s", cap_id)
        if isinstance(plugin, BusinessCapability):
            return plugin
        return plugin

    def unregister(self, capability_id: str) -> bool:
        """Unregisters a capability."""
        cap_id = capability_id.lower()
        if cap_id in self._plugins:
            del self._plugins[cap_id]
            self._enabled.pop(cap_id, None)
            return True
        return False

    def enable(self, capability_id: str) -> None:
        """Enables a capability."""
        self._enabled[capability_id.lower()] = True

    def disable(self, capability_id: str) -> None:
        """Disables a capability."""
        self._enabled[capability_id.lower()] = False

    def is_enabled(self, capability_id: str) -> bool:
        """Checks if capability is enabled."""
        return self._enabled.get(capability_id.lower(), True)

    def resolve(self, capability_id: str) -> Any | None:
        """Resolves active capability plugin."""
        cap_id = capability_id.lower()
        if self._enabled.get(cap_id, False):
            return self._plugins.get(cap_id)
        return None

    def get(self, capability_id: str) -> Any | None:
        """Alias for resolve()."""
        return self.resolve(capability_id)

    def find(self, capability_id: str) -> Any | None:
        """Alias for resolve()."""
        return self.resolve(capability_id)

    def find_by_id(self, capability_id: str) -> BusinessCapability | None:
        """Finds capability and returns BusinessCapability object."""
        res = self.resolve(capability_id)
        if not res:
            return None
        if isinstance(res, BusinessCapability):
            return res
        cap_id = str(getattr(res, "capability_id", capability_id))
        version = str(getattr(res, "version", "1.0.0"))
        return BusinessCapability(
            id=cap_id,
            name=cap_id.capitalize(),
            status="active",
            version=version,
        )

    def exists(self, capability_id: str) -> bool:
        """Checks if active capability exists."""
        return self.resolve(capability_id) is not None

    def contains(self, capability_id: str) -> bool:
        """Alias for exists()."""
        return self.exists(capability_id)

    def list_all(self) -> list[BusinessCapability]:
        """Returns list of all active BusinessCapabilities."""
        return [bc for cap_id in list(self._plugins.keys()) if (bc := self.find_by_id(cap_id)) is not None]

    def list_capabilities(self) -> list[CapabilityMetadata]:
        """Returns metadata list for runtime discovery."""
        return [p.metadata for p in self._plugins.values() if hasattr(p, "metadata") and p.metadata is not None]


# Backward compatibility alias
CapabilityRegistry = EnterpriseCapabilityRegistry
