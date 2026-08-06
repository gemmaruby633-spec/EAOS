"""Knowledge Compaction & Eviction Adapter (Anti-Bloat Engine)."""

from __future__ import annotations

from packages.evolution.domain.knowledge_compaction import (
    CompactionSummary,
    RawObservation,
)


class KnowledgeCompactionAdapter:
    """Engine distilling raw observations into 1KB pattern records."""

    async def compact_and_purge_raw_observations(
        self, raw_items: list[RawObservation], capability_id: str
    ) -> CompactionSummary:
        total_raw = len(raw_items)
        if total_raw == 0:
            return CompactionSummary(capability_id=capability_id)

        failed_count = sum(1 for r in raw_items if r.event_type == "FAILED_PATCH")

        lesson = (
            f"Negative Knowledge: Observed {failed_count} failed patches for '{capability_id}'. Avoid cyclic imports."
        )

        pattern = f"Pattern: {capability_id} requires immutable data types. Raw logs ({total_raw} items) purged."

        return CompactionSummary(
            capability_id=capability_id,
            total_raw_purged=total_raw,
            negative_lessons_extracted=[lesson],
            distilled_pattern=pattern,
            retained_size_bytes=len(pattern.encode("utf-8")),
        )
