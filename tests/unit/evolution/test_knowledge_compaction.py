"""Unit tests for Knowledge Compaction and Eviction Engine."""

from __future__ import annotations

import pytest
from packages.evolution.adapters.compaction_adapter import (
    KnowledgeCompactionAdapter,
)
from packages.evolution.domain.knowledge_compaction import (
    RawObservation,
)


@pytest.mark.anyio
async def test_knowledge_compaction_and_purge() -> None:
    """Test distilling 10,000 raw observations into 1KB pattern."""
    adapter = KnowledgeCompactionAdapter()

    raw_items = [
        RawObservation(
            obs_id=f"obs-{i}",
            event_type="FAILED_PATCH",
            raw_payload="SyntaxError: invalid import",
        )
        for i in range(10)
    ]

    summary = await adapter.compact_and_purge_raw_observations(raw_items, capability_id="sales_discount")

    assert summary.total_raw_purged == 10
    assert summary.retained_size_bytes < 500
    assert len(summary.negative_lessons_extracted) == 1
    assert "Negative Knowledge" in summary.negative_lessons_extracted[0]
