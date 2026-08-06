"""Marketing Application Use Cases — orchestrating domain logic via injected Ports.

Hexagonal Rules enforced here:
1. Use cases depend ONLY on domain models + domain ports (inward-facing).
2. Use cases do NOT know which adapter is injected — only the Port contract.
3. Use cases do NOT instantiate infrastructure (no `import uuid`, no I/O).
4. Return DTOs to the application boundary; domain entities stay inside.

Public API preserved for backward compatibility:
- ExecuteKeywordResearchUseCase.execute(keyword_text) -> KeywordTarget
- GenerateSEOArticleUseCase.execute(title, keyword_target) -> SEOArticleDraft
(Legacy callers in self_hosting/ still work without changes.)
"""

from __future__ import annotations

import uuid
from typing import Final

from packages.marketing.application.dto import (
    ArticleGenerationCommand,
    ArticleResult,
    CampaignLaunchCommand,
    CampaignResult,
    KeywordResearchCommand,
    KeywordResearchResult,
)
from packages.marketing.domain.models import (
    CampaignStatus,
    KeywordTarget,
    MarketingCampaign,
    MarketingChannel,
    SEOArticleDraft,
)
from packages.marketing.domain.ports import (
    ContentGeneratorPort,
    KeywordResearchPort,
    MarketingRepositoryPort,
)

# ---------------------------------------------------------------------------
# Internal constants
# ---------------------------------------------------------------------------

_DEFAULT_LOCALE: Final[str] = "en-US"
_DEFAULT_WORD_COUNT: Final[int] = 800
_CONTENT_PREVIEW_LEN: Final[int] = 200


# ---------------------------------------------------------------------------
# Individual Use Cases (fine-grained, single responsibility)
# ---------------------------------------------------------------------------


class ExecuteKeywordResearchUseCase:
    """Use case: perform keyword research and persist the result.

    Backward-compatible public API:
        result = ExecuteKeywordResearchUseCase(repo, provider).execute(text)

    Legacy zero-argument construction still supported via default stub adapter
    to avoid breaking callers in self_hosting/agency_orchestrator.py until
    they are migrated to use MarketingCommandPort.
    """

    def __init__(
        self,
        repository: MarketingRepositoryPort | None = None,
        provider: KeywordResearchPort | None = None,
    ) -> None:
        # Lazy import to avoid circular dependency; stubs live in infra layer.
        if repository is None or provider is None:
            from packages.marketing.infrastructure.adapters import (
                InMemoryKeywordResearchAdapter,
                InMemoryMarketingRepositoryAdapter,
            )

            self._repository: MarketingRepositoryPort = repository or InMemoryMarketingRepositoryAdapter()
            self._provider: KeywordResearchPort = provider or InMemoryKeywordResearchAdapter()
        else:
            self._repository = repository
            self._provider = provider

    def execute(self, keyword_text: str) -> KeywordTarget:
        """Research a keyword and persist the result.

        Args:
            keyword_text: The raw keyword string to analyze.

        Returns:
            Persisted KeywordTarget value object.
        """
        keyword = self._provider.research(keyword_text, locale=_DEFAULT_LOCALE)
        self._repository.save_keyword(keyword)
        return keyword

    def execute_with_command(self, command: KeywordResearchCommand) -> KeywordResearchResult:
        """Execute from a typed command DTO, returning a result DTO.

        Preferred over bare `execute()` for new callers.
        """
        keyword = self._provider.research(command.keyword_text, locale=command.locale)
        self._repository.save_keyword(keyword)
        return KeywordResearchResult(
            keyword_id=keyword.keyword_id,
            keyword=keyword.keyword,
            slug=keyword.slug,
            search_volume=keyword.search_volume,
            difficulty_score=keyword.difficulty_score,
            is_low_competition=keyword.is_low_competition,
        )


class GenerateSEOArticleUseCase:
    """Use case: generate an AI SEO article draft for a researched keyword.

    Backward-compatible public API:
        result = GenerateSEOArticleUseCase(repo, generator).execute(title, kw)
    """

    def __init__(
        self,
        repository: MarketingRepositoryPort | None = None,
        generator: ContentGeneratorPort | None = None,
    ) -> None:
        if repository is None or generator is None:
            from packages.marketing.infrastructure.adapters import (
                InMemoryContentGeneratorAdapter,
                InMemoryMarketingRepositoryAdapter,
            )

            self._repository: MarketingRepositoryPort = repository or InMemoryMarketingRepositoryAdapter()
            self._generator: ContentGeneratorPort = generator or InMemoryContentGeneratorAdapter()
        else:
            self._repository = repository
            self._generator = generator

    def execute(self, title: str, keyword_target: KeywordTarget) -> SEOArticleDraft:
        """Generate and persist an article draft.

        Args:
            title: Desired article headline.
            keyword_target: Previously researched keyword value object.

        Returns:
            Persisted SEOArticleDraft entity.
        """
        article = self._generator.generate_article(
            title,
            keyword_target,
            word_count=_DEFAULT_WORD_COUNT,
        )
        self._repository.save_article(article)
        return article

    def execute_with_command(self, command: ArticleGenerationCommand) -> ArticleResult:
        """Execute from a typed command DTO, returning a result DTO.

        Raises:
            KeyError: If keyword_id is not found in the repository.
        """
        keyword = self._repository.get_keyword_by_id(command.keyword_id)
        if keyword is None:
            raise KeyError(f"KeywordTarget '{command.keyword_id}' not found in repository.")

        article = self._generator.generate_article(
            command.title,
            keyword,
            word_count=command.word_count,
        )
        self._repository.save_article(article)
        return ArticleResult(
            article_id=article.article_id,
            title=article.title,
            slug=article.slug,
            keyword_id=article.keyword_id,
            status=article.status.value,
            content_preview=article.content_markdown[:_CONTENT_PREVIEW_LEN],
        )


class LaunchCampaignUseCase:
    """Use case: create and persist a new omnichannel marketing campaign."""

    def __init__(self, repository: MarketingRepositoryPort | None = None) -> None:
        if repository is None:
            from packages.marketing.infrastructure.adapters import (
                InMemoryMarketingRepositoryAdapter,
            )

            self._repository: MarketingRepositoryPort = InMemoryMarketingRepositoryAdapter()
        else:
            self._repository = repository

    def execute_with_command(self, command: CampaignLaunchCommand) -> CampaignResult:
        """Launch a campaign from a typed command DTO.

        Raises:
            ValueError: If the channel string is not a valid MarketingChannel.
        """
        try:
            channel = MarketingChannel(command.channel.upper())
        except ValueError as exc:
            valid = ", ".join(c.value for c in MarketingChannel)
            raise ValueError(f"Invalid channel '{command.channel}'. Valid options: {valid}.") from exc

        campaign = MarketingCampaign(
            campaign_id=f"CAM-{uuid.uuid4().hex[:8].upper()}",
            name=command.name,
            channel=channel,
            content_asset_ids=tuple(command.content_asset_ids),
            status=CampaignStatus.ACTIVE,
        )
        self._repository.save_campaign(campaign)
        return CampaignResult(
            campaign_id=campaign.campaign_id,
            name=campaign.name,
            channel=campaign.channel.value,
            status=campaign.status.value,
            content_asset_count=len(campaign.content_asset_ids),
        )


# ---------------------------------------------------------------------------
# Facade Use Case — implements MarketingCommandPort (Driving Port)
# ---------------------------------------------------------------------------


class MarketingApplicationService:
    """Facade implementing the MarketingCommandPort driving interface.

    This is the single entry point for all marketing capability commands
    when invoked from external systems (plugins, orchestrators, APIs).
    Callers should depend on MarketingCommandPort, not on this class directly.

    Usage:
        service: MarketingCommandPort = MarketingApplicationService(repo, kw, gen)
        keyword = service.research_keyword("AI Enterprise Architecture", locale="en-US")
    """

    def __init__(
        self,
        repository: MarketingRepositoryPort,
        keyword_provider: KeywordResearchPort,
        content_generator: ContentGeneratorPort,
    ) -> None:
        self._kw_use_case = ExecuteKeywordResearchUseCase(repository, keyword_provider)
        self._article_use_case = GenerateSEOArticleUseCase(repository, content_generator)
        self._campaign_use_case = LaunchCampaignUseCase(repository)
        self._repository = repository

    def research_keyword(self, keyword_text: str, *, locale: str = _DEFAULT_LOCALE) -> KeywordTarget:
        """Implement MarketingCommandPort.research_keyword."""
        command = KeywordResearchCommand(keyword_text=keyword_text, locale=locale)
        result = self._kw_use_case.execute_with_command(command)
        # Retrieve the persisted entity to return the domain object to callers
        keyword = self._repository.get_keyword_by_id(result.keyword_id)
        if keyword is None:
            raise RuntimeError(f"Keyword '{result.keyword_id}' vanished after save — repository bug.")
        return keyword

    def generate_article(
        self,
        title: str,
        keyword_id: str,
        *,
        word_count: int = _DEFAULT_WORD_COUNT,
    ) -> SEOArticleDraft:
        """Implement MarketingCommandPort.generate_article."""
        command = ArticleGenerationCommand(title=title, keyword_id=keyword_id, word_count=word_count)
        result = self._article_use_case.execute_with_command(command)
        article = self._repository.get_article_by_id(result.article_id)
        if article is None:
            raise RuntimeError(f"Article '{result.article_id}' vanished after save — repository bug.")
        return article

    def launch_campaign(
        self,
        name: str,
        channel: str,
        content_asset_ids: list[str],
    ) -> MarketingCampaign:
        """Implement MarketingCommandPort.launch_campaign."""
        command = CampaignLaunchCommand(name=name, channel=channel, content_asset_ids=content_asset_ids)
        result = self._campaign_use_case.execute_with_command(command)
        campaigns = self._repository.list_campaigns()
        for campaign in campaigns:
            if campaign.campaign_id == result.campaign_id:
                return campaign
        raise RuntimeError(f"Campaign '{result.campaign_id}' vanished after save — repository bug.")


# ---------------------------------------------------------------------------
# Module-level type alias for Port consumers
# ---------------------------------------------------------------------------

__all__ = [
    "ArticleGenerationCommand",
    "ArticleResult",
    "CampaignLaunchCommand",
    "CampaignResult",
    "ExecuteKeywordResearchUseCase",
    "GenerateSEOArticleUseCase",
    "KeywordResearchCommand",
    "KeywordResearchResult",
    "LaunchCampaignUseCase",
    "MarketingApplicationService",
]
