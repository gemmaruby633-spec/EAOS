"""Knowledge Valuation & Lifecycle Adapter (Knowledge Economy)."""

from __future__ import annotations

from packages.evolution.domain.knowledge_economy import (
    KnowledgeLifecycleDecision,
    KnowledgeValuation,
)


class KnowledgeValuationAdapter:
    """Adapter evaluating knowledge utility and managing lifecycles."""

    async def evaluate_asset_utility(self, asset: KnowledgeValuation) -> KnowledgeLifecycleDecision:
        cost = max(asset.maintenance_cost, 0.01)
        utility = (asset.confidence_score * asset.business_impact * (1 + asset.reuse_count)) / cost

        if utility >= 10.0:
            action = "KEEP"
            reason = "High business utility and high reuse count."
        elif utility >= 2.0:
            action = "ARCHIVE"
            reason = "Moderate utility; transition to Cold Archive."
        elif utility >= 0.5:
            action = "MERGE"
            reason = "Low utility; candidate for pattern consolidation."
        else:
            action = "FORGET"
            reason = "Low utility, high maintenance cost; purge asset."

        return KnowledgeLifecycleDecision(
            asset_id=asset.asset_id,
            action=action,
            utility_score=round(utility, 2),
            reasoning=reason,
        )
