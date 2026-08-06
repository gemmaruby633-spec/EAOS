"""Động cơ Quản lý và Truy vấn Danh mục Sản phẩm."""

from __future__ import annotations

from catalog.models import EnterpriseProduct, ProductTier


class CatalogEngine:
    """Động cơ tra cứu và quản lý SKU/Sản phẩm."""

    def __init__(self) -> None:
        self._products: dict[str, EnterpriseProduct] = {}

    def register_product(self, product_id: str, code: str, name: str) -> EnterpriseProduct:
        """Đăng ký sản phẩm mới vào danh mục."""
        product = EnterpriseProduct(product_id=product_id, code=code, name=name)
        self._products[product_id] = product
        return product

    def add_tier_to_product(self, product_id: str, tier: ProductTier) -> None:
        """Thêm gói cước giá cho sản phẩm."""
        if product_id not in self._products:
            raise KeyError(f"Product {product_id} không tồn tại.")
        self._products[product_id].tiers.append(tier)
