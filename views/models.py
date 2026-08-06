"""Mô hình DTO cho hệ thống Biểu diễn và Trình chiếu View (VIEWS)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ViewFormat(StrEnum):
    """Định dạng xuất chiếu View."""

    JSON = "JSON"
    MERMAID = "MERMAID"
    SVG = "SVG"
    HTML = "HTML"


@dataclass(frozen=True)
class ViewDefinition:
    """Thẻ chứa thông tin đặc tả View."""

    view_id: str
    title: str
    category: str
    raw_json: str


@dataclass
class RenderResult:
    """Kết quả xuất chiếu View."""

    view_id: str
    format: ViewFormat
    rendered_content: str
    proof_hash: str = ""
