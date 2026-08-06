"""Master Multi-Enterprise Ecosystem Orchestrator Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ecosystem.federation.federation_sync import FederationSyncEngine
from ecosystem.marketplace.capability_marketplace import (
    EcosystemCapabilityMarketplace,
)
from ecosystem.registry.registry_engine import (
    EcosystemMemberDTO,
    EcosystemRegistryEngine,
)
from ecosystem.trust.verifier import (
    EcosystemTrustVerifier,
)


class EcosystemSummaryDTO(BaseModel):
    """Summary DTO for multi-enterprise ecosystem status."""

    model_config = ConfigDict(frozen=True)

    total_member_nodes: int = Field(default=1)
    total_published_capabilities: int = Field(default=1)
    trust_verification_passed: bool = Field(default=True)
    members: list[EcosystemMemberDTO] = Field(default_factory=list)


class EAOSEcosystemEngine:
    """Master Orchestrator for Trust, Registry, Federation, & Marketplace."""

    def __init__(self) -> None:
        self.trust = EcosystemTrustVerifier()
        self.registry = EcosystemRegistryEngine()
        self.federation = FederationSyncEngine()
        self.marketplace = EcosystemCapabilityMarketplace()

    def get_ecosystem_summary(self) -> EcosystemSummaryDTO:
        """Generate master ecosystem operational summary."""
        members = self.registry.list_members()
        caps = self.marketplace.list_published_capabilities()
        attestation = self.trust.verify_enterprise_trust("ent-node-01")

        return EcosystemSummaryDTO(
            total_member_nodes=len(members),
            total_published_capabilities=len(caps),
            trust_verification_passed=attestation.is_verified,
            members=members,
        )
