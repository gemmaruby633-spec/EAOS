"""Marketing Infrastructure Adapters — concrete implementations of domain Ports.

Hexagonal Rules enforced here:
1. Adapters implement domain Ports (inward dependency).
2. Adapters MAY import infrastructure libraries (httpx, sqlalchemy, etc.).
3. Adapters MUST NOT be imported by domain/ or application/ layers directly.
   (Use cases receive adapters via constructor injection only.)

Provided adapters:
- InMemoryKeywordResearchAdapter  : stub keyword provider (no external I/O)
- InMemoryContentGeneratorAdapter : stub content generator (no external I/O)
- InMemoryMarketingRepositoryAdapter : thread-safe dict-based repository
"""

from __future__ import annotations

import uuid
from threading import Lock

from packages.marketing.domain.models import (
    ArticleStatus,
    KeywordTarget,
    MarketingCampaign,
    SEOArticleDraft,
)
from packages.marketing.domain.ports import (
    ContentGeneratorPort,
    KeywordResearchPort,
    MarketingRepositoryPort,
)

# ---------------------------------------------------------------------------
# Stub / In-Memory Secondary Adapters (Driven — SPI side)
# ---------------------------------------------------------------------------


class InMemoryKeywordResearchAdapter:
    """Stub adapter providing deterministic keyword metrics without I/O.

    Implements: KeywordResearchPort

    Production replacement: SEMrushKeywordAdapter, AhrefsKeywordAdapter, etc.
    """

    def research(self, keyword_text: str, *, locale: str) -> KeywordTarget:
        """Return a deterministic stub KeywordTarget for the given keyword.

        Search volume and difficulty are derived from the keyword length
        so tests remain deterministic without external API calls.
        """
        kw_id = f"KW-{uuid.uuid4().hex[:8].upper()}"
        # Deterministic but plausible stub metrics
        stub_volume = max(100, (len(keyword_text) * 150) % 10_000)
        stub_difficulty = round(min(95.0, len(keyword_text) * 2.5), 1)
        return KeywordTarget(
            keyword_id=kw_id,
            keyword=keyword_text,
            search_volume=stub_volume,
            difficulty_score=stub_difficulty,
        )


# Runtime check that the class satisfies the Protocol contract
assert isinstance(InMemoryKeywordResearchAdapter(), KeywordResearchPort)


class InMemoryContentGeneratorAdapter:
    """Stub adapter generating SEO article drafts locally without LLM calls.

    Implements: ContentGeneratorPort

    Production replacement: OllamaContentAdapter, OpenAIContentAdapter, etc.
    """

    def generate_article(
        self,
        title: str,
        keyword: KeywordTarget,
        *,
        word_count: int,
    ) -> SEOArticleDraft:
        """Generate a minimal stub article for the given keyword and title."""
        art_id = f"ART-{uuid.uuid4().hex[:8].upper()}"
        body = (
            f"# {title}\n\n"
            f"Target keyword: **{keyword.keyword}** "
            f"(volume: {keyword.search_volume}, difficulty: {keyword.difficulty_score}).\n\n"
            + ("Lorem ipsum dolor sit amet. " * (word_count // 6))
        )
        return SEOArticleDraft(
            article_id=art_id,
            title=title,
            slug=keyword.slug,
            keyword_id=keyword.keyword_id,
            content_markdown=body,
            status=ArticleStatus.DRAFT,
        )


assert isinstance(InMemoryContentGeneratorAdapter(), ContentGeneratorPort)


class InMemoryMarketingRepositoryAdapter:
    """Thread-safe in-memory repository for marketing aggregates.

    Implements: MarketingRepositoryPort

    Production replacement: SQLAlchemyMarketingRepository, MongoMarketingRepository, etc.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._keywords: dict[str, KeywordTarget] = {}
        self._articles: dict[str, SEOArticleDraft] = {}
        self._campaigns: dict[str, MarketingCampaign] = {}

    def save_keyword(self, keyword: KeywordTarget) -> None:
        """Persist keyword target (upsert by keyword_id)."""
        with self._lock:
            self._keywords[keyword.keyword_id] = keyword

    def save_article(self, article: SEOArticleDraft) -> None:
        """Persist article draft (upsert by article_id)."""
        with self._lock:
            self._articles[article.article_id] = article

    def save_campaign(self, campaign: MarketingCampaign) -> None:
        """Persist campaign (upsert by campaign_id)."""
        with self._lock:
            self._campaigns[campaign.campaign_id] = campaign

    def get_keyword_by_id(self, keyword_id: str) -> KeywordTarget | None:
        """Return keyword target by ID, or None if not found."""
        with self._lock:
            return self._keywords.get(keyword_id)

    def get_article_by_id(self, article_id: str) -> SEOArticleDraft | None:
        """Return article draft by ID, or None if not found."""
        with self._lock:
            return self._articles.get(article_id)

    def list_campaigns(self) -> list[MarketingCampaign]:
        """Return a snapshot of all stored campaigns."""
        with self._lock:
            return list(self._campaigns.values())


assert isinstance(InMemoryMarketingRepositoryAdapter(), MarketingRepositoryPort)


__all__ = [
    "InMemoryContentGeneratorAdapter",
    "InMemoryKeywordResearchAdapter",
    "InMemoryMarketingRepositoryAdapter",
]
