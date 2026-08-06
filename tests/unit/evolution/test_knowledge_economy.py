"""Unit tests for Knowledge Economy and Valuation Engine."""

from __future__ import annotations

import pytest
from packages.evolution.adapters.knowledge_valuation_adapter import (
    KnowledgeValuationAdapter,
)
from packages.evolution.domain.knowledge_economy import (
    KnowledgeValuation,
)


@pytest.mark.anyio
async def test_knowledge_valuation_and_lifecycle() -> None:
    """Test asset utility evaluation for KEEP and FORGET actions."""
    adapter = KnowledgeValuationAdapter()

    valuable_asset = KnowledgeValuation(
        asset_id="asset-001",
        category="ARCHITECTURE",
        confidence_score=0.95,
        business_impact=2.0,
        reuse_count=10,
        maintenance_cost=0.1,
    )

    decision = await adapter.evaluate_asset_utility(valuable_asset)
    assert decision.action == "KEEP"
    assert decision.utility_score > 10.0

    low_val_asset = KnowledgeValuation(
        asset_id="asset-002",
        category="OBSERVATION_NOISE",
        confidence_score=0.1,
        business_impact=0.1,
        reuse_count=0,
        maintenance_cost=1.0,
    )

    low_decision = await adapter.evaluate_asset_utility(low_val_asset)
    assert low_decision.action == "FORGET"
    assert low_decision.utility_score < 0.5
