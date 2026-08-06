"""Master Consolidated Platform Services Engine."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from platforms.platform_abstraction import (
    UnifiedPlatformAbstractionEngine,
)
from platforms.telemetry.collectors.telemetry_collector import (
    TelemetryCollectorEngine,
)


class PlatformSummaryDTO(BaseModel):
    """Summary DTO for consolidated platform services status."""

    model_config = ConfigDict(frozen=True)

    platform_status: str = Field(default="CONSOLIDATED_ACTIVE")
    total_services_count: int = Field(default=13)
    post_quantum_security_active: bool = Field(default=True)


class EAOSMasterPlatformEngine:
    """Master Orchestrator binding all consolidated platform services."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.abstraction = UnifiedPlatformAbstractionEngine()
        self.collector = TelemetryCollectorEngine()

    def get_platform_summary(self) -> PlatformSummaryDTO:
        """Generate master platform services summary."""
        return PlatformSummaryDTO(
            platform_status="CONSOLIDATED_ACTIVE",
            total_services_count=13,
            post_quantum_security_active=True,
        )
