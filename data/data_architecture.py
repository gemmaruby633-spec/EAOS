"""Master Data Architecture Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from data.governance.data_governance import DataGovernanceEngine
from data.lineage.data_lineage import DataLineageEngine
from data.quality.data_quality import DataQualityAuditor


class DataArchitectureSummaryDTO(BaseModel):
    """Summary DTO for enterprise data architecture."""

    model_config = ConfigDict(frozen=True)

    governance_active: bool = Field(default=True)
    lineage_tracked: bool = Field(default=True)
    quality_passed: bool = Field(default=True)


class EAOSDataArchitectureEngine:
    """Master Engine orchestrating Governance, Lineage, and Quality."""

    def __init__(self) -> None:
        self.governance = DataGovernanceEngine()
        self.lineage = DataLineageEngine()
        self.quality = DataQualityAuditor()

    def get_architecture_summary(self) -> DataArchitectureSummaryDTO:
        """Return data architecture operational status."""
        q_report = self.quality.audit_dataset("global_lake")
        return DataArchitectureSummaryDTO(
            governance_active=True,
            lineage_tracked=True,
            quality_passed=q_report.passed,
        )
