"""Mô phỏng biến động giá và tác động danh mục sản phẩm."""

from __future__ import annotations

from typing import Any


class DryRunSimulator:
    """Động cơ mô phỏng thay đổi giá và SKU an toàn."""

    @staticmethod
    def simulate_price_adjustment(
        catalog_prices: dict[str, float],
        price_changes: dict[str, float],
    ) -> dict[str, Any]:
        """Mô phỏng điều chỉnh giá sản phẩm."""
        simulated = catalog_prices.copy()
        warnings: list[str] = []

        for sku, delta in price_changes.items():
            current = simulated.get(sku, 0.0)
            new_price = current + delta
            if new_price <= 0:
                warnings.append(f"SKU {sku} giá sau điều chỉnh ({new_price}) <= 0")
            simulated[sku] = new_price

        return {
            "is_valid": len(warnings) == 0,
            "warnings": warnings,
            "simulated_prices": simulated,
        }
