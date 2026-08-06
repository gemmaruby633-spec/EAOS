"""Master Platforms Unified Engine Orchestrator."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from platforms.abstraction.platform_abstraction import (
    PlatformAbstractionEngine,
)
from platforms.security.post_quantum_signer import PostQuantumSignerEngine
from platforms.telemetry.observability import TelemetryService


class PlatformSummaryDTO(BaseModel):
    """Summary DTO for unified platform status."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(default="ACTIVE")
    post_quantum_security_active: bool = Field(default=True)
    telemetry_active: bool = Field(default=True)


class EAOSPlatformMasterEngine:
    """Master Orchestrator for Abstraction, Security, Telemetry & DB."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.abstraction = PlatformAbstractionEngine()
        self.security = PostQuantumSignerEngine()
        self.telemetry = TelemetryService()

    def get_platform_summary(self) -> PlatformSummaryDTO:
        """Generate master unified platform summary."""
        return PlatformSummaryDTO(
            status="ACTIVE",
            post_quantum_security_active=True,
            telemetry_active=True,
        )
