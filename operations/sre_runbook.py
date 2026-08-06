"""Master SRE and Operations Orchestrator Engine."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from operations.finops.finops_cost_tracker import (
    FinOpsCostTrackerEngine,
)
from operations.incident.incident_response import (
    IncidentResponseEngine,
)
from operations.runbooks.runbook_executor import (
    ExecutableRunbookEngine,
)
from operations.sre.sre_engine import SREEngine


class OperationsSummaryDTO(BaseModel):
    """Summary DTO for overall SRE operations health."""

    model_config = ConfigDict(frozen=True)

    sre_availability_score: float = Field(default=100.0)
    active_incidents_count: int = Field(default=0)
    runbook_execution_status: str = Field(default="READY")


class EAOSOperationsEngine:
    """Master Orchestrator for SRE, Incidents, FinOps, & Runbooks."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.sre = SREEngine()
        self.incident = IncidentResponseEngine()
        self.finops = FinOpsCostTrackerEngine()
        self.runbooks = ExecutableRunbookEngine(self.root)

    def get_operations_summary(self) -> OperationsSummaryDTO:
        """Generate master SRE operations summary."""
        sre_metric = self.sre.calculate_sre_health()
        rb_result = self.runbooks.execute_backup_runbook()

        return OperationsSummaryDTO(
            sre_availability_score=sre_metric.availability_score,
            active_incidents_count=0,
            runbook_execution_status=rb_result.status,
        )
