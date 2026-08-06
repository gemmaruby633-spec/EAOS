"""Unit tests for memory/ package."""

from __future__ import annotations

from pathlib import Path

from memory.architectural.architectural_memory import (
    ArchitecturalMemoryEngine,
)
from memory.enterprise_memory import EAOSEnterpriseMemoryEngine
from memory.vector.vector_memory import HybridVectorMemoryEngine


def test_architectural_memory_engine() -> None:
    """Test storing architectural memory record."""
    engine = ArchitecturalMemoryEngine()
    rec = engine.store_adr_memory("ADR-UI-001", "Contracts vs Imp")

    assert rec.adr_id == "ADR-UI-001"
    assert rec.memory_id.startswith("mem-arch-")


def test_hybrid_vector_memory_engine() -> None:
    """Test vector memory search."""
    engine = HybridVectorMemoryEngine()
    matches = engine.search_vector_memory("Architecture Rules")

    assert len(matches) == 1
    assert matches[0].similarity_score == 0.98


def test_enterprise_memory_engine_summary(tmp_path: Path) -> None:
    """Test master enterprise memory summary generation."""
    engine = EAOSEnterpriseMemoryEngine(workspace_root=tmp_path)
    summary = engine.get_memory_summary()

    assert summary.architectural_records_count >= 1
    assert summary.vector_search_active is True
