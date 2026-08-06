"""Unit tests for catalog/ package."""

from __future__ import annotations

from catalog.domain_element_catalog import DomainElementCatalogEngine


def test_domain_element_catalog_engine_summary() -> None:
    """Test master domain element catalog generation."""
    engine = DomainElementCatalogEngine()
    summary = engine.generate_catalog_summary()

    assert summary.total_aggregates >= 2
    assert summary.total_entities >= 2
    assert summary.total_commands >= 2
    assert summary.total_queries >= 1
    assert summary.total_events >= 1
    assert summary.aggregates[0].root_entity == "Customer"
