"""Mô hình DTO Quản lý Ngân sách Đầu tư."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InvestmentBucket:
    """Thùng ngân sách phân bổ theo chiến lược."""

    bucket_id: str
    name: str
    allocated_capital: float
    risk_tolerance: float


@dataclass(frozen=True)
class ValuationResult:
    """Kết quả định giá Tùy chọn Thực (Real Options Valuation)."""

    npv: float
    option_value: float
    simulated_volatility: float
    quantum_evidence_hash: str
