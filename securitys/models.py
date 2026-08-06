"""Mô hình DTO cho hệ thống An ninh Mật mã Doanh nghiệp (SECURITY)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SecurityLevel(StrEnum):
    """Mức độ bảo mật."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class IdentityToken:
    """Thẻ nhận dạng IAM."""

    subject_id: str
    roles: list[str]
    issuer: str = "EAOS_AUTH"


@dataclass
class AttestationProof:
    """Bằng chứng xác thực Zero-Knowledge."""

    proof_id: str
    is_valid: bool
    quantum_hash: str
