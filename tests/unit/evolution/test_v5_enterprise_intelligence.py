"""Unit tests for v5.x Enterprise Intelligence Economy Engine."""

from __future__ import annotations

import pytest
from packages.evolution.adapters.intelligence_economy_adapter import (
    EnterpriseIntelligenceAdapter,
)
from packages.evolution.domain.enterprise_intelligence import (
    EnterpriseIntelligenceAsset,
    KnowledgeDNA,
    KnowledgeGravity,
)


@pytest.mark.anyio
async def test_knowledge_gravity_and_natural_selection() -> None:
    """Test Knowledge Gravity calculation and Natural Selection."""
    adapter = EnterpriseIntelligenceAdapter()

    dna = KnowledgeDNA(origin_source="Incident Analysis")

    strong_asset = EnterpriseIntelligenceAsset(
        asset_id="asset-high",
        title="Immutable Data Pattern",
        dna=dna,
        gravity=KnowledgeGravity(
            reuse_count=50,
            citation_count=20,
            business_impact_score=2.0,
            success_rate=0.98,
        ),
    )

    weak_asset = EnterpriseIntelligenceAsset(
        asset_id="asset-low",
        title="Legacy Hack Rule",
        dna=dna,
        gravity=KnowledgeGravity(
            reuse_count=1,
            citation_count=0,
            business_impact_score=0.1,
            success_rate=0.30,
        ),
    )

    retained, retired = await adapter.execute_natural_selection([strong_asset, weak_asset])

    assert len(retained) == 1
    assert retained[0].asset_id == "asset-high"
    assert "asset-low" in retired


@pytest.mark.anyio
async def test_semantic_compression() -> None:
    """Test compressing intelligence items into high-level principle."""
    adapter = EnterpriseIntelligenceAdapter()
    compressed = await adapter.perform_semantic_compression(["Item 1", "Item 2", "Item 3"])

    assert "Principle:" in compressed
    assert "3 intelligence items" in compressed
