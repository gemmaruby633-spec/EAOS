"""Marketing Capability Plugin — infrastructure entry point for the Capability Bus.

Hexagonal Fix (V-03):
BEFORE (violation):
    from packages.capability.domain.models import EnterpriseCapabilityContext  # cross-pkg domain
    from packages.marketing.application.use_cases import ExecuteKeywordResearchUseCase  # infra→app

AFTER (compliant):
    - CapabilityExecutionContext defined locally as a Protocol structural type.
    - All marketing logic accessed via the MarketingCommandPort driving interface.
    - Zero cross-package domain coupling.

This plugin is the ONLY infrastructure entry point from the Capability Bus.
It translates external commands into MarketingCommandPort calls.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from packages.marketing.domain.models import (
    MarketingCampaign,
    MarketingChannel,
)
from packages.marketing.domain.ports import MarketingCommandPort

# ---------------------------------------------------------------------------
# Local structural Protocol — avoids coupling to capability.domain
# ---------------------------------------------------------------------------


@runtime_checkable
class CapabilityExecutionContext(Protocol):
    """Structural contract for the enterprise execution context.

    This Protocol mirrors the fields of EnterpriseCapabilityContext from the
    capability package without importing it. Structural subtyping ensures
    compatibility at runtime via isinstance() checks when needed.
    """

    tenant_id: str
    organization_id: str
    trace_id: str
    environment: str


# ---------------------------------------------------------------------------
# Supported action identifiers
# ---------------------------------------------------------------------------

_ACTION_RESEARCH_KEYWORD: str = "research_keyword"
_ACTION_GENERATE_ARTICLE: str = "generate_article"
_ACTION_LAUNCH_CAMPAIGN: str = "launch_campaign"

_SUPPORTED_ACTIONS: frozenset[str] = frozenset(
    {_ACTION_RESEARCH_KEYWORD, _ACTION_GENERATE_ARTICLE, _ACTION_LAUNCH_CAMPAIGN}
)


# ---------------------------------------------------------------------------
# Plugin Implementation
# ---------------------------------------------------------------------------


class MarketingCapabilityPlugin:
    """Infrastructure adapter bridging the Capability Bus to Marketing domain.

    Receives commands from the Capability Bus (external driving side) and
    delegates to the MarketingCommandPort (the marketing hexagon's primary port).

    Dependency injection via constructor:
        plugin = MarketingCapabilityPlugin(command_port=marketing_service)

    If no command_port is provided, the plugin self-wires with in-memory
    adapters (suitable for development and testing).
    """

    def __init__(self, command_port: MarketingCommandPort | None = None) -> None:
        if command_port is None:
            from packages.marketing.application.use_cases import (
                MarketingApplicationService,
            )
            from packages.marketing.infrastructure.adapters import (
                InMemoryContentGeneratorAdapter,
                InMemoryKeywordResearchAdapter,
                InMemoryMarketingRepositoryAdapter,
            )

            _repo = InMemoryMarketingRepositoryAdapter()
            _kw = InMemoryKeywordResearchAdapter()
            _gen = InMemoryContentGeneratorAdapter()
            self._port: MarketingCommandPort = MarketingApplicationService(_repo, _kw, _gen)
        else:
            self._port = command_port

    # ------------------------------------------------------------------
    # Capability Bus Protocol surface
    # ------------------------------------------------------------------

    @property
    def capability_id(self) -> str:
        """Unique identifier registered in the Capability Bus."""
        return "marketing"

    @property
    def version(self) -> str:
        """Semantic version of this plugin implementation."""
        return "2.0.0"

    def supports_action(self, action: str) -> bool:
        """Return True if this plugin handles the given action identifier."""
        return action in _SUPPORTED_ACTIONS

    def execute(
        self,
        action: str,
        context: CapabilityExecutionContext,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Dispatch an action through the MarketingCommandPort.

        Args:
            action: Action identifier string (must be a supported action).
            context: Execution context carrying tenant, trace, and env data.
            payload: Action-specific input data dictionary.

        Returns:
            Serialized result as a plain dict (JSON-compatible).

        Raises:
            ValueError: If the action is not supported.
        """
        if action == _ACTION_RESEARCH_KEYWORD:
            return self._handle_research_keyword(payload, context)
        if action == _ACTION_GENERATE_ARTICLE:
            return self._handle_generate_article(payload, context)
        if action == _ACTION_LAUNCH_CAMPAIGN:
            return self._handle_launch_campaign(payload, context)

        raise ValueError(f"Unsupported action '{action}'. Supported: {', '.join(sorted(_SUPPORTED_ACTIONS))}.")

    # ------------------------------------------------------------------
    # Private action handlers
    # ------------------------------------------------------------------

    def _handle_research_keyword(
        self,
        payload: dict[str, Any],
        context: CapabilityExecutionContext,
    ) -> dict[str, Any]:
        keyword_text = str(payload.get("keyword", "AI Enterprise"))
        locale = str(payload.get("locale", "en-US"))
        result = self._port.research_keyword(keyword_text, locale=locale)
        return {
            "keyword_id": result.keyword_id,
            "keyword": result.keyword,
            "slug": result.slug,
            "search_volume": result.search_volume,
            "difficulty_score": result.difficulty_score,
            "is_low_competition": result.is_low_competition,
            "trace_id": context.trace_id,
        }

    def _handle_generate_article(
        self,
        payload: dict[str, Any],
        context: CapabilityExecutionContext,
    ) -> dict[str, Any]:
        title = str(payload.get("title", "Untitled Article"))
        keyword_id = str(payload.get("keyword_id", ""))
        word_count = int(payload.get("word_count", 800))
        result = self._port.generate_article(title, keyword_id, word_count=word_count)
        return {
            "article_id": result.article_id,
            "title": result.title,
            "slug": result.slug,
            "status": result.status.value,
            "keyword_id": result.keyword_id,
            "trace_id": context.trace_id,
        }

    def _handle_launch_campaign(
        self,
        payload: dict[str, Any],
        context: CapabilityExecutionContext,
    ) -> dict[str, Any]:
        name = str(payload.get("name", "New Campaign"))
        channel_raw = str(payload.get("channel", MarketingChannel.ORGANIC_SEO.value))
        asset_ids: list[str] = [str(a) for a in payload.get("content_asset_ids", [])]
        result: MarketingCampaign = self._port.launch_campaign(name, channel_raw, asset_ids)
        return {
            "campaign_id": result.campaign_id,
            "name": result.name,
            "channel": result.channel.value,
            "status": result.status.value,
            "content_asset_count": len(result.content_asset_ids),
            "trace_id": context.trace_id,
        }


__all__ = [
    "CapabilityExecutionContext",
    "MarketingCapabilityPlugin",
]
