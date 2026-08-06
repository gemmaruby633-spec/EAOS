"""Unit tests for Compiler Solidification (Semantic Analysis & Fitness)."""

from __future__ import annotations

import pytest
from packages.business_architecture.domain.meta_model import (
    EnterpriseMetaModel,
    EntityMeta,
)
from packages.business_architecture.domain.semantic_analyzer import (
    SemanticAnalyzer,
)
from packages.governance.adapters.compiler_fitness_adapter import (
    CompilerFitnessInspectorAdapter,
)


def test_semantic_analyzer_detects_duplicates() -> None:
    """Test semantic analyzer detects duplicate entities/capabilities."""
    meta = EnterpriseMetaModel(
        enterprise_name="EAOS",
        capabilities=["Sales", "Sales"],
        entities=[
            EntityMeta(name="Customer"),
            EntityMeta(name="Customer"),
        ],
    )
    analyzer = SemanticAnalyzer()
    report = analyzer.analyze(meta)

    assert report.passed is False
    assert len(report.errors) == 2
    assert "Duplicate capability" in report.errors[0]
    assert "Duplicate entity" in report.errors[1]


@pytest.mark.anyio
async def test_compiler_fitness_inspector() -> None:
    """Test compiler architectural fitness rules."""
    inspector = CompilerFitnessInspectorAdapter()
    report = await inspector.inspect_compiler_architecture()

    assert report.score == 100.0
    assert report.passed is True
