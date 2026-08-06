"""Master Operating Model Registry Engine (BIZBOK / OMC)."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from operatingmodel.organization.organization_engine import (
    OrganizationEngine,
)
from operatingmodel.processes.process_architecture import (
    ProcessArchitectureEngine,
)
from operatingmodel.roles.role_matrix import RoleMatrixEngine
from operatingmodel.services.operating_service import (
    OperatingServiceEngine,
)
from operatingmodel.value_streams.value_stream_engine import (
    ValueStreamDTO,
    ValueStreamEngine,
)


class OperatingModelSummaryDTO(BaseModel):
    """Summary DTO for enterprise operating model health."""

    model_config = ConfigDict(frozen=True)

    total_value_streams: int = Field(default=1)
    total_org_units: int = Field(default=2)
    total_processes: int = Field(default=1)
    total_roles: int = Field(default=1)
    total_services: int = Field(default=1)
    value_stream: ValueStreamDTO


class OperatingModelRegistryEngine:
    """Master Engine orchestrating Value Streams, Org, Processes, & Roles."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.value_streams = ValueStreamEngine()
        self.org = OrganizationEngine()
        self.processes = ProcessArchitectureEngine()
        self.roles = RoleMatrixEngine()
        self.services = OperatingServiceEngine()

    def get_operating_model_summary(self) -> OperatingModelSummaryDTO:
        """Generate master operating model summary."""
        vs = self.value_streams.get_lead_to_cash_stream()
        orgs = self.org.list_business_units()
        procs = self.processes.list_core_processes()
        rls = self.roles.list_operating_roles()
        svcs = self.services.list_operating_services()

        return OperatingModelSummaryDTO(
            total_value_streams=1,
            total_org_units=len(orgs),
            total_processes=len(procs),
            total_roles=len(rls),
            total_services=len(svcs),
            value_stream=vs,
        )
