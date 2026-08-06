"""Mô hình Vòng đời Sản phẩm (Product Lifecycle Management - PLM)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProductStage(StrEnum):
    """Các giai đoạn vòng đời sản phẩm."""

    CONCEPT = "CONCEPT"
    DEVELOPMENT = "DEVELOPMENT"
    GENERAL_AVAILABILITY = "GENERAL_AVAILABILITY"
    DEPRECATED = "DEPRECATED"
    END_OF_LIFE = "END_OF_LIFE"


@dataclass
class ProductLifecycleState:
    """Mô tả trạng thái PLM của sản phẩm."""

    product_id: str
    current_stage: ProductStage
    quantum_proof_hash: str
