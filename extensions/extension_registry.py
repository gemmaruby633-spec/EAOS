"""Master Extensions Registry Engine Orchestrator."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from extensions.plugins.plugin_manager import (
    DynamicPluginManager,
    ExtensionPluginDTO,
)


class ExtensionRegistrySummaryDTO(BaseModel):
    """Summary DTO for overall extension framework status."""

    model_config = ConfigDict(frozen=True)

    total_connectors: int = Field(default=0)
    total_drivers: int = Field(default=0)
    total_plugins: int = Field(default=1)
    plugins: list[ExtensionPluginDTO] = Field(default_factory=list)


class EAOSExtensionsEngine:
    """Master Engine orchestrating Connectors, Drivers, and Plugins."""

    def __init__(self) -> None:
        self.plugin_manager = DynamicPluginManager()

    def get_extensions_summary(self) -> ExtensionRegistrySummaryDTO:
        """Generate summary of registered extensions."""
        plugins = self.plugin_manager.list_active_plugins()
        return ExtensionRegistrySummaryDTO(
            total_connectors=0,
            total_drivers=0,
            total_plugins=len(plugins),
            plugins=plugins,
        )
