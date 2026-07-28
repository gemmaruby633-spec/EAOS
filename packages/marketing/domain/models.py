"""Marketing Capability Domain Models for EAOS."""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class KeywordTarget(BaseModel):
    """Value object representing a targeted SEO keyword."""

    model_config = ConfigDict(frozen=True)

    keyword_id: str = Field(..., description="Unique Keyword ID")
    keyword: str = Field(..., description="Search keyword text")
    search_volume: int = Field(default=0)
    difficulty_score: float = Field(default=0.0)


class SEOArticleDraft(BaseModel):
    """Entity representing an AI-generated SEO article draft."""

    model_config = ConfigDict(frozen=True)

    article_id: str = Field(..., description="Unique Article ID")
    title: str = Field(..., description="Article title")
    slug: str = Field(..., description="SEO URL slug")
    keyword_id: str = Field(..., description="Target keyword ID")
    content_markdown: str = Field(..., description="Body content")
    status: str = Field(default="DRAFT")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MarketingCampaign(BaseModel):
    """Entity representing an omnichannel marketing campaign."""

    model_config = ConfigDict(frozen=True)

    campaign_id: str = Field(..., description="Unique Campaign ID")
    name: str = Field(..., description="Campaign name")
    channel: str = Field(..., description="GOOGLE, FACEBOOK, EMAIL")
    content_asset_ids: list[str] = Field(default_factory=list)
    status: str = Field(default="ACTIVE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
