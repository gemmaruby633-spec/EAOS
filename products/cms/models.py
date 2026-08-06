"""Mô hình DTO cho Content Management System (CMS)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ContentStatus(StrEnum):
    """Trạng thái xuất bản của nội dung."""

    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


@dataclass
class ContentNode:
    """Nút nội dung CMS Headless."""

    content_id: str
    title: str
    slug: str
    body: str
    status: ContentStatus = ContentStatus.DRAFT
    metadata: dict[str, str] = field(default_factory=dict)
