"""Unit tests for digitaltwin/ package."""

from __future__ import annotations

from digitaltwin.twin_orchestrator import (
    EnterpriseDigitalTwinOrchestrator,
)


def test_digital_twin_orchestrator_state_and_simulation() -> None:
    """Test digital twin state capture and simulation execution."""
    orchestrator = EnterpriseDigitalTwinOrchestrator()
    state = orchestrator.get_current_twin_state()

    assert state.overall_health_score == 100.0
    assert state.active_components_count == 3
    assert state.components[0].component_id == "api_gateway"

    sim_res = orchestrator.simulate_change("Deploy Policy Patch v2")
    assert sim_res.policy_compliant is True
    assert sim_res.risk_level == "LOW"
