"""Mô hình DTO Enterprise Resource Planning (ERP)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InventoryItem:
    """Mô hình vật tư hàng hóa ERP."""

    sku: str
    name: str
    quantity_on_hand: float
    unit_cost: float


@dataclass(frozen=True)
class LedgerEntry:
    """Sổ cái kế toán ghi nhận giao dịch ERP."""

    entry_id: str
    account_code: str
    amount: float
    description: str
