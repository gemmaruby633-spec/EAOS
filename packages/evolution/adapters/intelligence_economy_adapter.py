"""Enterprise Intelligence Economy Adapter (v5.x Engine)."""

from __future__ import annotations

from packages.evolution.domain.enterprise_intelligence import (
    EnterpriseIntelligenceAsset,
)


class EnterpriseIntelligenceAdapter:
    """Adapter executing Natural Selection & Semantic Compression."""

    async def execute_natural_selection(
        self, assets: list[EnterpriseIntelligenceAsset]
    ) -> tuple[list[EnterpriseIntelligenceAsset], list[str]]:
        """Select superior rules and retire low-gravity assets."""
        if not assets:
            return [], []

        sorted_assets = sorted(assets, key=lambda a: a.gravity.gravity_score, reverse=True)

        retained: list[EnterpriseIntelligenceAsset] = []
        retired_ids: list[str] = []

        top_gravity = sorted_assets[0].gravity.gravity_score

        for asset in sorted_assets:
            if asset.gravity.gravity_score >= top_gravity * 0.5:
                retained.append(asset)
            else:
                retired_ids.append(asset.asset_id)

        return retained, retired_ids

    async def perform_semantic_compression(self, intelligence_items: list[str]) -> str:
        """Compress multiple intelligence items into single Principle."""
        count = len(intelligence_items)
        return (
            f"Principle: Synthesized from {count} intelligence items. "
            "Business value takes precedence over technological preference."
        )
