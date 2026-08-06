"""Comprehensive unit tests for all operations/ submodules."""

from __future__ import annotations

from operations.capabilities.backup.backup_capability import (
    BackupCapabilityDTO,
)
from operations.capabilities.incident.incident_capability import (
    IncidentCapabilityDTO,
)
from operations.capabilities.monitoring.monitoring_capability import (
    MonitoringCapabilityDTO,
)
from operations.capabilities.recovery.recovery_capability import (
    RecoveryCapabilityDTO,
)
from operations.constitution.principles.ops_principles import (
    OperationsPrinciplesDTO,
)
from operations.digital_twin.simulations.ops_simulation import (
    OpsSimulationDTO,
)
from operations.evolution.fitness_functions.ops_fitness import (
    OpsFitnessDTO,
)
from operations.governance.policies.ops_policy import OpsPolicyDTO
from operations.governance.workflows.ops_workflow import (
    OpsWorkflowDTO,
)
from operations.knowledge.ontology.ops_ontology import (
    OpsOntologyDTO,
)
from operations.observability.metrics.ops_metrics import OpsMetricsDTO
from operations.playbooks.ops_playbook import OpsPlaybookDTO
from operations.sre_runbook import EAOSOperationsEngine


def test_all_operations_submodules() -> None:
    """Verify all operations/ submodules instantiation."""
    assert BackupCapabilityDTO().status == "ACTIVE"
    assert IncidentCapabilityDTO().status == "ACTIVE"
    assert MonitoringCapabilityDTO().status == "ACTIVE"
    assert RecoveryCapabilityDTO().status == "ACTIVE"
    assert OperationsPrinciplesDTO().principle == "Zero-Ops Automation"
    assert OpsSimulationDTO().status == "SIMULATED_PASS"
    assert OpsFitnessDTO().score == 100.0
    assert OpsPolicyDTO().policy_id == "POL-OPS-01"
    assert OpsWorkflowDTO().workflow_id == "WF-OPS-01"
    assert OpsOntologyDTO().concept == "OperationalExcellence"
    assert OpsMetricsDTO().metric_name == "ops_latency"
    assert OpsPlaybookDTO().title == "Disaster Recovery Playbook"


def test_operations_engine_summary() -> None:
    """Test master SRE operations engine summary generation."""
    engine = EAOSOperationsEngine()
    summary = engine.get_operations_summary()

    assert summary.sre_availability_score == 100.0
    assert summary.active_incidents_count == 0
    assert summary.runbook_execution_status == "COMPLETED"
