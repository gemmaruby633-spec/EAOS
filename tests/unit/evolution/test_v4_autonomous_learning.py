"""Unit tests for v4.x Autonomous Learning & Evolution Architecture."""

from __future__ import annotations

import pytest
from packages.evolution.adapters.enterprise_learning_adapter import (
    EnterpriseLearningAdapter,
)
from packages.evolution.domain.enterprise_memory import (
    EnterpriseMemoryRecord,
    MemoryCategory,
)


@pytest.mark.anyio
async def test_enterprise_learning_pipeline() -> None:
    """Test storing 10-category memory, pattern mining, and ADR proposals."""
    adapter = EnterpriseLearningAdapter()

    mem = EnterpriseMemoryRecord(
        memory_id="mem-001",
        category=MemoryCategory.ARCHITECTURE,
        capability_id="cap-evolution",
        evidence_summary="Linter RUF012 detected mutable class attributes.",
        root_cause="Class attributes declared as mutable sets.",
        corrective_action="Refactored to ClassVar[frozenset[str]].",
        preventive_action="Enforce ClassVar AST fitness rule.",
        lessons=["Use ClassVar or instance attributes in Python 3.14."],
    )

    saved = await adapter.store_enterprise_memory(mem)
    assert saved is True

    mined = await adapter.mine_incident_patterns([mem])
    assert mined.mined_patterns_count == 1
    assert len(mined.candidate_rules) == 1
    assert mined.candidate_rules[0].approved is True

    adrs = await adapter.recommend_adr_evolution(mined)
    assert len(adrs) == 1
    assert "ADR-EVO-" in adrs[0]
