"""Động cơ ERP quản lý tồn kho và sổ cái tài nguyên."""

from __future__ import annotations

from erp.models import InventoryItem, LedgerEntry


class ErpEngine:
    """Động cơ hoạch định tài nguyên doanh nghiệp."""

    def __init__(self) -> None:
        self._inventory: dict[str, InventoryItem] = {}
        self._ledger: list[LedgerEntry] = []

    def add_inventory(
        self,
        sku: str,
        name: str,
        quantity: float,
        unit_cost: float,
    ) -> InventoryItem:
        """Thêm mới tồn kho sản phẩm."""
        item = InventoryItem(
            sku=sku,
            name=name,
            quantity_on_hand=quantity,
            unit_cost=unit_cost,
        )
        self._inventory[sku] = item
        return item

    def record_ledger_entry(
        self,
        entry_id: str,
        account_code: str,
        amount: float,
        description: str,
    ) -> LedgerEntry:
        """Ghi nhận bút toán tài chính ERP."""
        entry = LedgerEntry(
            entry_id=entry_id,
            account_code=account_code,
            amount=amount,
            description=description,
        )
        self._ledger.append(entry)
        return entry
