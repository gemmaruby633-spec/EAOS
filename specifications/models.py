"""Mô hình DTO cho hệ thống Executable Specifications (SPECIFICATIONS)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class SpecCategory(StrEnum):
    """Phân loại Specification."""

    APIS = "APIS"
    BUSINESS = "BUSINESS"
    CAPABILITIES = "CAPABILITIES"
    DOMAINS = "DOMAINS"
    SERVICES = "SERVICES"
    WORKFLOWS = "WORKFLOWS"


@dataclass(frozen=True)
class SpecificationRecord:
    """Thẻ lưu trữ Đặc tả."""

    spec_id: str
    title: str
    category: SpecCategory
    file_path: str


@dataclass
class SpecComplianceResult:
    """Kết quả kiểm tra tuân thủ Đặc tả."""

    spec_id: str
    is_compliant: bool
    violations: list[str] = field(default_factory=list)
    proof_hash: str = ""
