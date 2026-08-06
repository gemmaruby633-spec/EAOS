"""Enterprise Learning Port Protocol (v4.x)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.evolution.domain.enterprise_memory import (
    EnterpriseMemoryRecord,
)
from packages.evolution.domain.pattern_mining import (
    PatternMiningResult,
)


@runtime_checkable
class EnterpriseLearningPort(Protocol):
    """Port protocol for 8-Engine Enterprise Learning System."""

    async def store_enterprise_memory(self, record: EnterpriseMemoryRecord) -> bool: ...

    async def mine_incident_patterns(self, memory_records: list[EnterpriseMemoryRecord]) -> PatternMiningResult: ...

    async def recommend_adr_evolution(self, pattern_result: PatternMiningResult) -> list[str]: ...
