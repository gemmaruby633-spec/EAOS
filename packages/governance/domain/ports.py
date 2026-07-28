"""Domain Ports and Value Objects for Enterprise Governance."""

from typing import Any, Protocol
from pydantic import BaseModel, ConfigDict


class ScanDiagnostic(BaseModel):
    """Diagnostic record for file scan or AST parse warnings/errors."""

    model_config = ConfigDict(frozen=True)

    file_path: str
    severity: str
    message: str


class TopologyScanDTO(BaseModel):
    """Raw workspace topology scan data containing AST imports and diagnostics."""

    model_config = ConfigDict(frozen=True)

    active_py_files: int
    empty_directories: int
    import_records: list[tuple[str, str]]
    diagnostics: list[ScanDiagnostic]


class AuditSnapshotDTO(BaseModel):
    """Persistent audit snapshot value object with real fitness metrics."""

    model_config = ConfigDict(frozen=True)

    canonical_layers_matched: int = 52
    capability_domains_count: int = 10
    sub_capability_packages: int = 58
    active_source_files: int
    empty_directories: int
    architecture_violations: int
    audit_warnings_count: int
    calculated_health_score: float
    coupling_index: float = 0.0
    instability_index: float = 0.0
    package_cohesion: float = 0.95
    audit_status: str
    diagnostics_summary: list[str]
    all_connected: bool = True
    isolated_directories_count: int = 0
    total_root_directories: int = 38
    constitution_version: str = "v3.0"
    timestamp: float


class TopologyScannerPort(Protocol):
    """Port for scanning workspace filesystem and extracting AST data."""

    def scan_workspace(self) -> TopologyScanDTO: ...


class GovernancePolicyProviderPort(Protocol):
    """Port for loading dynamic governance policies."""

    def load_policy(self) -> dict[str, Any]: ...


class GovernanceRepositoryPort(Protocol):
    """Port for persisting snapshots and querying historical trends."""

    def save_snapshot(self, snapshot: AuditSnapshotDTO) -> None: ...

    def get_latest_snapshot(self) -> AuditSnapshotDTO | None: ...

    def get_snapshot_history(self) -> list[AuditSnapshotDTO]: ...


class KnowledgeGraphPort(Protocol):
    """Port for querying live Knowledge Graph metrics from Neo4j."""

    def query_system_node_count(self) -> int: ...
