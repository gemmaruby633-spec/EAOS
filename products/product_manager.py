"""Lớp Facade hợp nhất toàn bộ các phân hệ Products."""

from __future__ import annotations

from typing import Any

from automation.dry_run_simulator import DryRunSimulator
from catalog.catalog_engine import CatalogEngine
from catalog.models import ProductTier
from cms.cms_engine import CmsEngine
from crm.crm_engine import CrmEngine
from erp.erp_engine import ErpEngine
from lifecycle.lifecycle_engine import LifecycleEngine


class ProductManager:
    """Facade quản lý tập trung toàn bộ Sản phẩm Doanh nghiệp."""

    def __init__(self) -> None:
        self.cms = CmsEngine()
        self.crm = CrmEngine()
        self.erp = ErpEngine()
        self.catalog = CatalogEngine()
        self.lifecycle = LifecycleEngine()

    def launch_new_product(
        self,
        product_id: str,
        code: str,
        name: str,
        default_price: float,
    ) -> dict[str, Any]:
        """Khởi tạo toàn bộ vòng đời sản phẩm mới."""
        prod = self.catalog.register_product(product_id, code, name)
        tier = ProductTier("tier_std", "Standard", default_price)
        self.catalog.add_tier_to_product(product_id, tier)

        state = self.lifecycle.initialize_product_lifecycle(product_id)

        return {
            "product_id": prod.product_id,
            "code": prod.code,
            "stage": state.current_stage.value,
            "proof_hash": state.quantum_proof_hash,
        }

    def simulate_pricing_change(
        self,
        current_prices: dict[str, float],
        deltas: dict[str, float],
    ) -> dict[str, Any]:
        """Mô phỏng thay đổi bảng giá sản phẩm."""
        return DryRunSimulator.simulate_price_adjustment(current_prices, deltas)
