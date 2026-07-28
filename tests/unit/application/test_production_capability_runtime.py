"""Unit tests verifying Production Capability Runtime Engine."""

from engine.capability.registry import CapabilityRegistry
from engine.capability.runtime import ProductionCapabilityRuntimeEngine
from packages.capability.domain.models import EnterpriseCommandDTO
from packages.marketing.infrastructure.plugin import (
    MarketingCapabilityPlugin,
)


def test_production_capability_runtime_success() -> None:
    """Verifies end-to-end execution through registry and plugin."""
    registry = CapabilityRegistry()
    registry.register(MarketingCapabilityPlugin())
    runtime = ProductionCapabilityRuntimeEngine(registry)

    cmd = EnterpriseCommandDTO(
        capability_id="marketing",
        action="research_keyword",
        payload={"keyword": "AI Digital Company"},
    )
    res = runtime.execute(cmd)

    assert res.status == "SUCCESS"
    assert res.capability_id == "marketing"
    assert res.action == "research_keyword"
    assert len(res.events_emitted) == 1
    assert res.events_emitted[0].event_type == "MARKETING_RESEARCH_KEYWORD_COMPLETED"
    assert res.events_emitted[0]["event_type"] == "MARKETING_RESEARCH_KEYWORD_COMPLETED"


def test_production_capability_runtime_unknown_capability() -> None:
    """Verifies graceful handling of unknown capabilities."""
    registry = CapabilityRegistry()
    runtime = ProductionCapabilityRuntimeEngine(registry)

    cmd = EnterpriseCommandDTO(
        capability_id="non_existent",
        action="do_something",
    )
    res = runtime.execute(cmd)

    assert res.status == "NOT_FOUND"
    assert "error" in res.payload
