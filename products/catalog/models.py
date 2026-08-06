"""Mô hình DTO Danh mục Sản phẩm Doanh nghiệp."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProductTier:
    """Cấp độ sản phẩm (Free, Pro, Enterprise)."""

    tier_id: str
    name: str
    monthly_price: float


@dataclass
class EnterpriseProduct:
    """Mô hình Sản phẩm Doanh nghiệp tổng thể."""

    product_id: str
    code: str
    name: str
    tiers: list[ProductTier] = field(default_factory=list)
    is_active: bool = True
