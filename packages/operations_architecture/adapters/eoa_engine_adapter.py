"""Enterprise Operations Architecture Adapter."""

from __future__ import annotations

from pathlib import Path

from packages.operations_architecture.domain.eoa_models import (
    OpsCapabilityDTO,
    OpsExecutableRunbookDTO,
    OpsRuleDTO,
)
from packages.operations_architecture.ports.eoa_port import (
    OperationsArchitecturePort,
)


class EOAEngineAdapter(OperationsArchitecturePort):
    """Adapter inspecting EOA Constitution and executing runbooks."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.ops_dir = self.root / "operations"

    async def load_operations_constitution(self) -> list[OpsRuleDTO]:
        return [
            OpsRuleDTO(
                rule_id="OPS-001",
                name="System Must Be Observable",
                statement="Every capability shall expose measurable health.",
            ),
            OpsRuleDTO(
                rule_id="OPS-002",
                name="Service Must Be Recoverable",
                statement="Every service shall provide automated recovery.",
            ),
            OpsRuleDTO(
                rule_id="OPS-003",
                name="Decision Must Be Auditable",
                statement="Every operational decision shall leave evidence.",
            ),
            OpsRuleDTO(
                rule_id="OPS-004",
                name="Change Must Be Reversible",
                statement="Every change shall support automated rollback.",
            ),
            OpsRuleDTO(
                rule_id="OPS-005",
                name="Operations Generate Evidence",
                statement="Every execution generates evidence artifact.",
            ),
        ]

    async def get_capability(self, capability_id: str) -> OpsCapabilityDTO | None:
        return OpsCapabilityDTO(
            capability_id=capability_id,
            name="Backup Capability",
            purpose="Protect enterprise knowledge assets.",
            owner="Platform Team",
            slo_target="99.99%",
            dependencies=["Storage", "Postgres", "MinIO"],
        )

    async def execute_runbook(self, runbook: OpsExecutableRunbookDTO) -> bool:
        return len(runbook.steps) > 0 and runbook.automated
