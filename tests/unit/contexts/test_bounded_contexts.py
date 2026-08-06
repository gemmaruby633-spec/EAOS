"""Unit tests for contexts/ package."""

from __future__ import annotations

from contexts.context_registry import BoundedContextRegistryEngine


def test_bounded_context_registry_engine() -> None:
    """Test generating master DDD context map."""
    engine = BoundedContextRegistryEngine()
    context_map = engine.generate_context_map()

    assert context_map.total_contexts >= 4
    assert len(context_map.relationships) >= 2
    assert context_map.contexts[0].context_id == "crm"
    assert context_map.relationships[0].upstream_context == "crm"
