"""Unit test suite for Capability Runtime Engine."""

from engine.capability.capability_runtime import (
    CapabilityExecutionCommandDTO,
    CapabilityRuntimeEngine,
)


def test_capability_runtime_execution() -> None:
    """Verifies dynamic capability command execution."""
    engine = CapabilityRuntimeEngine()
    cmd = CapabilityExecutionCommandDTO(
        capability_id="marketing",
        action="generate_article",
        payload={"title": "AI Enterprise"},
    )
    res = engine.execute_capability(cmd)

    assert res.capability_id == "marketing"
    assert res.action == "generate_article"
    assert res.success is True
    assert res.result_data["status"] == "EXECUTED"
