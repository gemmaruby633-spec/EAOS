"""Mô hình DTO cho hệ thống Mã nguồn Cốt lõi (SRC)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceDomainSnapshot:
    """Ảnh chụp trạng thái phân lớp Clean Architecture."""

    total_aggregates: int
    total_use_cases: int
    is_pure_domain: bool
    quantum_proof: str
