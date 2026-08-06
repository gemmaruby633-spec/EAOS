"""Mô hình dữ liệu Quản lý Chương trình (Programs)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PortfolioProgram:
    """Mô hình Chương trình quản lý nhiều chuỗi giá trị."""

    program_id: str
    name: str
    lead_architect: str
    dependencies: list[str] = field(default_factory=list)
