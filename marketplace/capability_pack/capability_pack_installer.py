"""Capability Pack Installer and Publisher Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CapabilityPackManifestDTO(BaseModel):
    """Value object representing a published Capability Pack manifest."""

    model_config = ConfigDict(frozen=True)

    pack_id: str = Field(..., description="Unique Pack ID")
    capability_name: str = Field(..., description="Capability name")
    version: str = Field(default="1.0.0")
    publisher: str = Field(default="EAOS Marketplace")
    is_installed: bool = Field(default=True)


class CapabilityPackInstallerEngine:
    """Engine installing and managing capability packs."""

    def list_available_capability_packs(
        self,
    ) -> list[CapabilityPackManifestDTO]:
        """Return available capability packs in marketplace."""
        return [
            CapabilityPackManifestDTO(
                pack_id="pack-cap-sales-discount",
                capability_name="Sales Discount Capability",
                version="1.0.0",
                publisher="EAOS Core",
            )
        ]
