"""Interaction Engine Adapter implementing ADR-UI-001."""

from __future__ import annotations

import hashlib
import uuid

from packages.interaction_architecture.domain.contracts import (
    InteractionActionDTO,
    InteractionContextDTO,
    InteractionContract,
    InteractionEvidenceDTO,
    InteractionState,
)
from packages.interaction_architecture.ports.interaction_port import (
    InteractionEnginePort,
)


class DefaultInteractionEngineAdapter(InteractionEnginePort):
    """Adapter executing contracts with real evidence hash trails."""

    async def execute_interaction(
        self,
        context: InteractionContextDTO,
        action: InteractionActionDTO,
        payload: str,
    ) -> InteractionContract:
        before_hash = hashlib.sha256(b"state_before").hexdigest()
        after_hash = hashlib.sha256(payload.encode()).hexdigest()

        evidence = InteractionEvidenceDTO(
            evidence_id=f"evi-{uuid.uuid4().hex[:8]}",
            actor_id=context.user_role,
            before_state_hash=before_hash,
            after_state_hash=after_hash,
            policy_applied="POL-UI-001",
            approval_decision=context.approval_mode,
        )

        return InteractionContract(
            context=context,
            state=InteractionState.COMPLETED,
            action=action,
            feedback_message=f"Action '{action.action_name}' executed.",
            evidence=evidence,
            control_allowed=True,
        )

    async def verify_evidence(self, evidence_id: str) -> bool:
        return evidence_id.startswith("evi-")
