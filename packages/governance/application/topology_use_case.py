"""Topology Audit Use Case calculating real graph-based fitness metrics."""

import time

from packages.governance.domain.fitness_metrics import FitnessMetricsCalculator
from packages.governance.domain.fitness_plugins import (
    FitnessRuleRegistry,
    GenericGovernancePolicyEngine,
)
from packages.governance.domain.ports import (
    AuditSnapshotDTO,
    GovernancePolicyProviderPort,
    GovernanceRepositoryPort,
    TopologyScannerPort,
)


class GovernanceAuditOrchestrator:
    """Orchestrator executing background audit pipeline on actual import graph."""

    def __init__(
        self,
        scanner: TopologyScannerPort,
        policy_provider: GovernancePolicyProviderPort,
        repository: GovernanceRepositoryPort,
        registry: FitnessRuleRegistry | None = None,
    ) -> None:
        self.scanner = scanner
        self.policy_provider = policy_provider
        self.repository = repository
        self.registry = registry or FitnessRuleRegistry()
        self.policy_engine = GenericGovernancePolicyEngine()
        self.metrics_calculator = FitnessMetricsCalculator()

    def run_pipeline(self) -> AuditSnapshotDTO:
        """Executes scan, calculates metrics from REAL import graph, persists snapshot."""
        scan_data = self.scanner.scan_workspace()
        policy = self.policy_provider.load_policy()

        # Dynamic fitness evaluation on real import records
        fitness_results = [plugin.evaluate(scan_data.import_records) for plugin in self.registry.get_all_plugins()]

        # Calculate actual graph coupling & instability
        graph_metrics = self.metrics_calculator.calculate_metrics(
            active_files_count=scan_data.active_py_files,
            import_records=scan_data.import_records,
        )

        diagnostics_count = len(scan_data.diagnostics)
        calculated_score = self.policy_engine.calculate_score(
            fitness_results=fitness_results,
            empty_dirs_count=scan_data.empty_directories,
            diagnostics_count=diagnostics_count,
            policy=policy,
        )

        violations_count = sum(r.violations_count for r in fitness_results)
        diag_summaries = [f"[{d.severity}] {d.file_path}: {d.message}" for d in scan_data.diagnostics]

        status = (
            "100% VALID - ZERO ARCHITECTURE DRIFT"
            if violations_count == 0 and diagnostics_count == 0
            else f"WARNING: {violations_count} VIOLATIONS, {diagnostics_count} ERRORS"
        )

        snapshot = AuditSnapshotDTO(
            active_source_files=scan_data.active_py_files,
            empty_directories=scan_data.empty_directories,
            architecture_violations=violations_count,
            audit_warnings_count=diagnostics_count,
            calculated_health_score=calculated_score,
            coupling_index=graph_metrics.coupling_index,
            instability_index=graph_metrics.instability_index,
            package_cohesion=graph_metrics.package_cohesion,
            audit_status=status,
            diagnostics_summary=diag_summaries,
            timestamp=time.time(),
        )

        self.repository.save_snapshot(snapshot)
        return snapshot


class TopologyAuditUseCase:
    """Application Use Case providing instant non-blocking snapshot reads."""

    def __init__(
        self,
        repository: GovernanceRepositoryPort,
        orchestrator: GovernanceAuditOrchestrator,
    ) -> None:
        self.repository = repository
        self.orchestrator = orchestrator

    def get_audit_report(self) -> AuditSnapshotDTO:
        snapshot = self.repository.get_latest_snapshot()
        if snapshot is None:
            snapshot = self.orchestrator.run_pipeline()
        return snapshot

    def trigger_audit_run(self) -> AuditSnapshotDTO:
        return self.orchestrator.run_pipeline()
