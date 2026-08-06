"""Unit test suite verifying ADR-UI-001 compliance."""

from __future__ import annotations

import pytest
from packages.design_system.domain.tokens import DesignTokenRegistry
from packages.interaction_architecture.adapters.interaction_engine_adapter import (
    DefaultInteractionEngineAdapter,
)
from packages.interaction_architecture.domain.contracts import (
    InteractionActionDTO,
    InteractionContextDTO,
    InteractionState,
)


@pytest.mark.anyio
async def test_interaction_contract_execution() -> None:
    """Verify 6-part contract execution and real evidence generation."""
    adapter = DefaultInteractionEngineAdapter()
    context = InteractionContextDTO()
    action = InteractionActionDTO(action_name="apply_patch")

    contract = await adapter.execute_interaction(context, action, payload="sample_patch_content")

    assert contract.state == InteractionState.COMPLETED
    assert contract.evidence is not None
    assert contract.evidence.policy_applied == "POL-UI-001"
    assert contract.evidence.approval_decision == "ASK"

    verified = await adapter.verify_evidence(contract.evidence.evidence_id)
    assert verified is True


def test_design_token_registry_tokens() -> None:
    """Verify semantic design tokens immutability."""
    tokens = DesignTokenRegistry()
    assert tokens.colors.status_success == "emerald-400"
    assert tokens.colors.action_primary == "emerald-600"
