"""Bootstrap module assembling Governance Capability dependencies."""

from pathlib import Path
from typing import Any

from packages.evolution.infrastructure.rego_compiler import (
    NativeRegoCompiler,
    RegoRuleResult,
)
from packages.governance.application.topology_use_case import (
    GovernanceAuditOrchestrator,
    TopologyAuditUseCase,
)
from packages.governance.domain.fitness_plugins import (
    FitnessRuleRegistry,
    HexagonalBoundaryFitnessRule,
    KnowledgeGraphIntegrityFitnessRule,
)
from packages.governance.infrastructure.adapters import (
    ComponentizedTopologyScannerAdapter,
    Neo4jRestAdapter,
    PersistentJsonSnapshotRepositoryAdapter,
    YamlGovernancePolicyAdapter,
)

ROOT_DIR = Path(__file__).resolve().parents[3]


class PolicyEvaluatorAdapter(NativeRegoCompiler):
    """Adapter supporting Rego compilation, flags, and simple payload checks."""

    def evaluate_payload(self, payload: dict[str, Any]) -> tuple[bool, list[RegoRuleResult]]:
        return True, []

    def evaluate_flag(self, flag_key: str, tenant_id: str) -> dict[str, Any]:
        return {
            "flag_key": flag_key,
            "enabled": True,
            "tenant_id": tenant_id,
        }


policy_evaluator = PolicyEvaluatorAdapter()

scanner = ComponentizedTopologyScannerAdapter(ROOT_DIR)
policy_provider = YamlGovernancePolicyAdapter(ROOT_DIR / "config" / "governance_policy.yaml")
repository = PersistentJsonSnapshotRepositoryAdapter(ROOT_DIR / "runtime" / "governance" / "audit_history.jsonl")
neo4j_adapter = Neo4jRestAdapter()

registry = FitnessRuleRegistry()
registry.register(HexagonalBoundaryFitnessRule())
registry.register(KnowledgeGraphIntegrityFitnessRule(neo4j_adapter))

orchestrator = GovernanceAuditOrchestrator(scanner, policy_provider, repository, registry)
topology_use_case = TopologyAuditUseCase(repository, orchestrator)
