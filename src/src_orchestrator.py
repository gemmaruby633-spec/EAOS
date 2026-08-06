"""Facade Orchestrator cho miền SRC."""

from __future__ import annotations

from typing import Any

from application.use_cases.evaluate_security_policy_use_case import (
    EvaluateSecurityPolicyUseCase,
)
from automation.dry_run_src_simulator import DryRunSrcSimulator
from infrastructure.ledger.quantum_src_ledger import QuantumSrcLedger
from infrastructure.persistence.in_memory_policy_repository import (
    InMemoryPolicyRepository,
)


class SrcOrchestrator:
    """Facade hợp nhất Clean Architecture cho phân hệ SRC."""

    def __init__(self) -> None:
        self.repository = InMemoryPolicyRepository()
        self.use_case = EvaluateSecurityPolicyUseCase(self.repository)

    def evaluate_policy(self, policy_id: str, resource: str) -> dict[str, Any]:
        """Đánh giá chính sách có đóng dấu chứng nhận mã hóa."""
        result = self.use_case.execute(policy_id, resource)
        proof = QuantumSrcLedger.generate_src_proof(policy_id, result)
        return {
            "policy_id": policy_id,
            "result": result,
            "quantum_proof": proof,
        }

    def simulate_policy_change(self, policy_id: str, new_rule_id: str) -> dict[str, Any]:
        """Mô phỏng thay đổi chính sách an toàn."""
        return DryRunSrcSimulator.simulate_change(policy_id, new_rule_id)
