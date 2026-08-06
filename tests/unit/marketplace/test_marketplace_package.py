"""Unit tests for marketplace/ package."""

from __future__ import annotations

from pathlib import Path

from marketplace.capability_pack.capability_pack_installer import (
    CapabilityPackInstallerEngine,
)
from marketplace.pack_registry import EcosystemPackRegistryEngine


def test_capability_pack_installer() -> None:
    """Test listing capability packs."""
    installer = CapabilityPackInstallerEngine()
    packs = installer.list_available_capability_packs()

    assert len(packs) >= 1
    assert packs[0].pack_id == "pack-cap-sales-discount"


def test_marketplace_pack_registry_engine(tmp_path: Path) -> None:
    """Test master marketplace summary generation."""
    engine = EcosystemPackRegistryEngine(workspace_root=tmp_path)
    summary = engine.get_marketplace_summary()

    assert summary.total_capability_packs >= 1
    assert summary.total_agent_packs >= 1
    assert summary.marketplace_active is True
