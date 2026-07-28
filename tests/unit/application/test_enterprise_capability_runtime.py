"""Unit tests verifying Enterprise Command Bus and Pipeline Runtime."""

from engine.capability.command_bus import EnterpriseCommandBus
from engine.capability.pipeline import CapabilityPipelineExecutor
from engine.capability.registry import EnterpriseCapabilityRegistry
from packages.capability.domain.models import EnterpriseCommandDTO
from packages.marketing.infrastructure.plugin import (
    MarketingCapabilityPlugin,
)


def test_enterprise_command_bus_pipeline_success() -> None:
    """Verifies end-to-end command dispatch through bus and pipeline."""
    registry = EnterpriseCapabilityRegistry()
    registry.register(MarketingCapabilityPlugin())
    pipeline = CapabilityPipelineExecutor(registry)
    bus = EnterpriseCommandBus(pipeline)

    cmd = EnterpriseCommandDTO(
        capability_id="marketing",
        action="research_keyword",
        payload={"keyword": "AI Enterprise OS"},
    )
    res = bus.dispatch(cmd)

    assert res.status == "SUCCESS"
    assert res.capability_id == "marketing"
    assert res.action == "research_keyword"
    assert len(res.events_emitted) == 1
    assert res.events_emitted[0].event_type == "MARKETING_RESEARCH_KEYWORD_COMPLETED"


def test_enterprise_pipeline_disabled_capability() -> None:
    """Verifies pipeline behavior when a capability is disabled."""
    registry = EnterpriseCapabilityRegistry()
    registry.register(MarketingCapabilityPlugin())
    registry.disable("marketing")

    pipeline = CapabilityPipelineExecutor(registry)
    bus = EnterpriseCommandBus(pipeline)

    cmd = EnterpriseCommandDTO(
        capability_id="marketing",
        action="research_keyword",
    )
    res = bus.dispatch(cmd)

    assert res.status == "NOT_FOUND"
