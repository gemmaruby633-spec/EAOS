"""Động cơ quản lý vòng đời Stage-Gate cho sản phẩm."""

from __future__ import annotations

from lifecycle.models import ProductLifecycleState, ProductStage
from lifecycle.quantum_product_ledger import QuantumProductLedger


class LifecycleEngine:
    """Động cơ PLM điều phối vòng đời sản phẩm."""

    def __init__(self) -> None:
        self._states: dict[str, ProductLifecycleState] = {}

    def initialize_product_lifecycle(self, product_id: str) -> ProductLifecycleState:
        """Khởi tạo vòng đời sản phẩm với mã băm bằng chứng."""
        proof = QuantumProductLedger.generate_product_proof(product_id, {"stage": "CONCEPT"})
        state = ProductLifecycleState(
            product_id=product_id,
            current_stage=ProductStage.CONCEPT,
            quantum_proof_hash=proof,
        )
        self._states[product_id] = state
        return state

    def transition_stage(self, product_id: str, next_stage: ProductStage) -> ProductLifecycleState:
        """Chuyển đổi giai đoạn vòng đời sản phẩm."""
        if product_id not in self._states:
            raise KeyError(f"Product {product_id} chưa khởi tạo PLM.")
        proof = QuantumProductLedger.generate_product_proof(product_id, {"stage": next_stage.value})
        state = ProductLifecycleState(
            product_id=product_id,
            current_stage=next_stage,
            quantum_proof_hash=proof,
        )
        self._states[product_id] = state
        return state
