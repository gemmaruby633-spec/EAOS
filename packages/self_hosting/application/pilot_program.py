"""Pilot Program Dynamic Evidence Collector for EAOS Operational Monitoring."""

import uuid
from datetime import UTC, datetime
from pathlib import Path

from packages.frameworks.application.architecture_validator import (
    ExecutableArchitectureValidator,
)
from pydantic import BaseModel, ConfigDict, Field


class RealPilotEvidenceReportDTO(BaseModel):
    """Value object representing real dynamic operational pilot evidence."""

    model_config = ConfigDict(frozen=True)

    pilot_id: str
    pilot_name: str
    version_tag: str
    total_source_files_count: int
    active_capability_packages_count: int
    real_drift_index: float
    is_architecture_clean: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EAOSPilotEvidenceCollector:
    """Collector dynamically aggregating real operational system metrics."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()
        self.validator = ExecutableArchitectureValidator(self.root_path)

    def collect_real_evidence(self, pilot_name: str) -> RealPilotEvidenceReportDTO:
        """Aggregates real-time file counts and architecture metrics."""
        val_report = self.validator.validate_repository()

        py_files = list(self.root_path.glob("**/*.py"))
        pkg_dir = self.root_path / "packages"
        pkgs = [d for d in pkg_dir.iterdir() if d.is_dir()] if pkg_dir.exists() else []

        p_id = f"PILOT-{uuid.uuid4().hex[:8].upper()}"
        drift = round((100.0 - val_report.fitness_score) / 100.0, 4)

        return RealPilotEvidenceReportDTO(
            pilot_id=p_id,
            pilot_name=pilot_name,
            version_tag="v1.0.0",
            total_source_files_count=len(py_files),
            active_capability_packages_count=len(pkgs),
            real_drift_index=drift,
            is_architecture_clean=val_report.is_compliant,
        )


if __name__ == "__main__":
    collector = EAOSPilotEvidenceCollector()
    report = collector.collect_real_evidence("AI_SOLOPRENEUR_DIGITAL_AGENCY")
    print(f"✔ Dynamic Pilot Evidence Report: {report.pilot_id}")
    print(f"  - Real Source Files Count : {report.total_source_files_count}")
    print(f"  - Active Packages Count   : {report.active_capability_packages_count}")
    print(f"  - Real Calculated Drift   : {report.real_drift_index}")
