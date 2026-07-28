"""Marketing Capability Plugin implementing CapabilityPluginProtocol."""

from typing import Any
from packages.capability.domain.models import (
    EnterpriseCapabilityContext,
)
from packages.marketing.application.use_cases import (
    ExecuteKeywordResearchUseCase,
)


class MarketingCapabilityPlugin:
    """Plugin wrapping Marketing Capability implementation."""

    @property
    def capability_id(self) -> str:
        """Returns capability ID."""
        return "marketing"

    @property
    def version(self) -> str:
        """Returns plugin version."""
        return "1.0.0"

    def supports_action(self, action: str) -> bool:
        """Checks if action is supported."""
        return action in ("research_keyword", "generate_campaign")

    def execute(
        self,
        action: str,
        context: EnterpriseCapabilityContext,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Executes marketing action."""
        if action == "research_keyword":
            kw = str(payload.get("keyword", "AI Enterprise"))
            use_case = ExecuteKeywordResearchUseCase()
            result = use_case.execute(kw)
            return result.model_dump()
        return {"status": "ACTION_EXECUTED"}
