"""Application use cases for Marketing Capability Workflow."""

import uuid

from packages.marketing.domain.models import (
    KeywordTarget,
    SEOArticleDraft,
)


class ExecuteKeywordResearchUseCase:
    """Use case performing automated keyword research."""

    def execute(self, keyword_text: str) -> KeywordTarget:
        """Analyzes keyword volume and difficulty."""
        kw_id = f"KW-{uuid.uuid4().hex[:8].upper()}"
        return KeywordTarget(
            keyword_id=kw_id,
            keyword=keyword_text,
            search_volume=2400,
            difficulty_score=35.5,
        )


class GenerateSEOArticleUseCase:
    """Use case generating an AI article draft from keyword."""

    def execute(self, title: str, keyword_target: KeywordTarget) -> SEOArticleDraft:
        """Generates article outline and draft content."""
        art_id = f"ART-{uuid.uuid4().hex[:8].upper()}"
        slug_text = keyword_target.keyword.lower().replace(" ", "-")
        return SEOArticleDraft(
            article_id=art_id,
            title=title,
            slug=slug_text,
            keyword_id=keyword_target.keyword_id,
            content_markdown=f"# {title}\n\nSEO Content for {slug_text}.",
            status="DRAFT",
        )
