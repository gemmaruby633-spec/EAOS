"""Marketing Capability Domain Ports (Hexagonal Interfaces).

Hexagonal Rule:
- Driving Ports (API)  = interfaces the application EXPOSES to the outside world.
- Driven Ports  (SPI)  = interfaces the application REQUIRES from infrastructure.

All ports are defined as typing.Protocol — no concrete implementations here.
Infrastructure adapters implement these protocols.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.marketing.domain.models import (
    KeywordTarget,
    MarketingCampaign,
    SEOArticleDraft,
)

# ---------------------------------------------------------------------------
# Driven Ports (SPI) — infrastructure must implement these
# ---------------------------------------------------------------------------


@runtime_checkable
class KeywordResearchPort(Protocol):
    """Secondary port: external keyword data provider.

    Implementors: SEMrush adapter, Ahrefs adapter, stub adapter, etc.
    """

    def research(
        self,
        keyword_text: str,
        *,
        locale: str,
    ) -> KeywordTarget:
        """Fetch keyword metrics for the given text and locale.

        Args:
            keyword_text: The raw keyword string to research.
            locale: BCP-47 locale tag (e.g. "en-US", "vi-VN").

        Returns:
            A fully populated KeywordTarget value object.
        """
        ...


@runtime_checkable
class ContentGeneratorPort(Protocol):
    """Secondary port: AI content generation provider.

    Implementors: Ollama adapter, OpenAI adapter, stub adapter, etc.
    """

    def generate_article(
        self,
        title: str,
        keyword: KeywordTarget,
        *,
        word_count: int,
    ) -> SEOArticleDraft:
        """Generate an SEO article draft for the given keyword target.

        Args:
            title: Desired article headline.
            keyword: Researched keyword value object.
            word_count: Target word count for the generated body.

        Returns:
            A new SEOArticleDraft entity in DRAFT status.
        """
        ...


@runtime_checkable
class MarketingRepositoryPort(Protocol):
    """Secondary port: persistence store for marketing aggregates.

    Implementors: SQLite adapter, in-memory adapter, PostgreSQL adapter, etc.
    """

    def save_keyword(self, keyword: KeywordTarget) -> None:
        """Persist a keyword target."""
        ...

    def save_article(self, article: SEOArticleDraft) -> None:
        """Persist an article draft."""
        ...

    def save_campaign(self, campaign: MarketingCampaign) -> None:
        """Persist a marketing campaign."""
        ...

    def get_keyword_by_id(self, keyword_id: str) -> KeywordTarget | None:
        """Retrieve a keyword target by its ID, or None if not found."""
        ...

    def get_article_by_id(self, article_id: str) -> SEOArticleDraft | None:
        """Retrieve an article draft by its ID, or None if not found."""
        ...

    def list_campaigns(self) -> list[MarketingCampaign]:
        """Return all stored campaigns."""
        ...


# ---------------------------------------------------------------------------
# Driving Port (API) — primary interface exposed to external callers
# ---------------------------------------------------------------------------


@runtime_checkable
class MarketingCommandPort(Protocol):
    """Primary port: entry point for all marketing capability commands.

    External systems (plugins, APIs, orchestrators) invoke this port.
    They must NOT bypass it to call use cases directly.
    """

    def research_keyword(
        self,
        keyword_text: str,
        *,
        locale: str,
    ) -> KeywordTarget:
        """Execute a keyword research command.

        Args:
            keyword_text: The keyword to research.
            locale: Target market locale (BCP-47).

        Returns:
            Researched keyword target value object.
        """
        ...

    def generate_article(
        self,
        title: str,
        keyword_id: str,
        *,
        word_count: int,
    ) -> SEOArticleDraft:
        """Execute an article generation command.

        Args:
            title: Desired article headline.
            keyword_id: ID of the previously researched keyword.
            word_count: Target word count.

        Returns:
            New SEO article draft entity.

        Raises:
            KeyError: If keyword_id does not exist in the repository.
        """
        ...

    def launch_campaign(
        self,
        name: str,
        channel: str,
        content_asset_ids: list[str],
    ) -> MarketingCampaign:
        """Execute a campaign launch command.

        Args:
            name: Human-readable campaign name.
            channel: Target channel identifier (maps to MarketingChannel enum).
            content_asset_ids: References to associated content assets.

        Returns:
            Newly created MarketingCampaign entity.
        """
        ...
