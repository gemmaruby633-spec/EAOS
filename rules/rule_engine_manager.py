"""Facade Orchestrator quản lý toàn bộ các động cơ Quy tắc."""

from __future__ import annotations

from typing import Any

from ai.ai_rule_engine import AiRuleEngine
from architecture.architecture_rule_engine import (
    ArchitectureRuleEngine,
)
from automation.dry_run_rule_simulator import (
    DryRunRuleSimulator,
)
from business.business_rule_engine import BusinessRuleEngine
from compliance.compliance_rule_engine import (
    ComplianceRuleEngine,
)
from engineering.engineering_rule_engine import (
    EngineeringRuleEngine,
)
from ledger.quantum_rule_audit import QuantumRuleAudit
from quality.quality_rule_engine import QualityRuleEngine
from runtime.runtime_rule_engine import RuntimeRuleEngine
from security.security_rule_engine import SecurityRuleEngine

from models import EvaluationResult


class RuleEngineManager:
    """Facade hợp nhất điều phối 8 phân hệ quy tắc doanh nghiệp."""

    def __init__(self) -> None:
        self.ai = AiRuleEngine()
        self.architecture = ArchitectureRuleEngine()
        self.business = BusinessRuleEngine()
        self.compliance = ComplianceRuleEngine()
        self.engineering = EngineeringRuleEngine()
        self.quality = QualityRuleEngine()
        self.runtime = RuntimeRuleEngine()
        self.security = SecurityRuleEngine()

    def run_full_governance_audit(self, context: dict[str, Any]) -> dict[str, Any]:
        """Thực thi toàn bộ 8 bộ kiểm toán quy tắc."""
        results: list[EvaluationResult] = []

        results.append(self.ai.evaluate_drift(context.get("drift_rate", 0.02)))
        results.append(self.architecture.evaluate_isolation(context.get("cross_imports", 0)))
        results.append(self.business.evaluate_order_value(context.get("order_value", 150.0)))
        results.append(self.compliance.evaluate_gdpr_retention(context.get("retention_days", 30)))
        results.append(self.engineering.evaluate_line_length(context.get("max_line_len", 78)))
        results.append(self.quality.evaluate_mypy_strict(context.get("typed_percent", 100.0)))
        results.append(self.runtime.evaluate_circuit_breaker(context.get("error_rate", 0.01)))
        results.append(self.security.evaluate_secret_scan(context.get("secrets_found", 0)))

        all_passed = all(r.passed for r in results)
        audit_proof = QuantumRuleAudit.generate_audit_proof(
            "GOV-AUDIT-FULL",
            {"passed": all_passed, "total_rules": len(results)},
        )

        return {
            "all_passed": all_passed,
            "total_rules_evaluated": len(results),
            "audit_proof_hash": audit_proof,
            "results": [
                {
                    "rule_id": r.rule_id,
                    "passed": r.passed,
                    "message": r.message,
                }
                for r in results
            ],
        }

    def simulate_rule_threshold(
        self,
        rule_name: str,
        current_threshold: float,
        proposed_threshold: float,
    ) -> dict[str, Any]:
        """Mô phỏng thay đổi ngưỡng quy tắc an toàn."""
        return DryRunRuleSimulator.simulate_threshold_change(rule_name, current_threshold, proposed_threshold)
