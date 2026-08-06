"""Động cơ CMS xuất bản và quản lý nội dung số."""

from __future__ import annotations

from cms.models import ContentNode, ContentStatus


class CmsEngine:
    """Động cơ xuất bản Headless Content Management."""

    def __init__(self) -> None:
        self._nodes: dict[str, ContentNode] = {}

    def create_content(
        self,
        content_id: str,
        title: str,
        slug: str,
        body: str,
    ) -> ContentNode:
        """Tạo mới nút nội dung."""
        node = ContentNode(
            content_id=content_id,
            title=title,
            slug=slug,
            body=body,
        )
        self._nodes[content_id] = node
        return node

    def publish_content(self, content_id: str) -> ContentNode:
        """Xuất bản nội dung."""
        if content_id not in self._nodes:
            raise KeyError(f"Content {content_id} không tồn tại.")
        node = self._nodes[content_id]
        node.status = ContentStatus.PUBLISHED
        return node
