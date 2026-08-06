"""Master Marketplace Pack Registry Engine Orchestrator."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from marketplace.agent_pack.agent_pack_installer import (
    AgentPackInstallerEngine,
)
from marketplace.capability_pack.capability_pack_installer import (
    CapabilityPackInstallerEngine,
    CapabilityPackManifestDTO,
)


class MarketplaceSummaryDTO(BaseModel):
    """Summary DTO for marketplace status."""

    model_config = ConfigDict(frozen=True)

    total_capability_packs: int = Field(default=1)
    total_agent_packs: int = Field(default=1)
    marketplace_active: bool = Field(default=True)
    capability_packs: list[CapabilityPackManifestDTO] = Field(default_factory=list)


class EcosystemPackRegistryEngine:
    """Master Engine orchestrating Capability, Agent, Policy, & Workflows."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.cap_installer = CapabilityPackInstallerEngine()
        self.agent_installer = AgentPackInstallerEngine()

    def get_marketplace_summary(self) -> MarketplaceSummaryDTO:
        """Generate master marketplace summary."""
        cap_packs = self.cap_installer.list_available_capability_packs()
        agent_packs = self.agent_installer.list_available_agent_packs()

        return MarketplaceSummaryDTO(
            total_capability_packs=len(cap_packs),
            total_agent_packs=len(agent_packs),
            marketplace_active=True,
            capability_packs=cap_packs,
        )
