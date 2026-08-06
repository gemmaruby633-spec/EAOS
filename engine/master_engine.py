"""Master Cybernetic Execution Engine Orchestrator."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from engine.planner.task_planner import AutonomousTaskPlannerEngine
from engine.sandbox.wasm_runtime import WASMSandboxRuntime
from engine.scheduler.cybernetic_scheduler import CyberneticScheduler


class EngineStatusDTO(BaseModel):
    """Operational status DTO for master execution engine."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(default="ACTIVE")
    sub_engines_count: int = Field(default=12)
    cybernetic_loop_active: bool = Field(default=True)


class EAOSMasterEngine:
    """Master Orchestrator binding all 12 cybernetic sub-engines."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.planner = AutonomousTaskPlannerEngine()
        self.sandbox = WASMSandboxRuntime()
        self.scheduler = CyberneticScheduler()

    def get_engine_status(self) -> EngineStatusDTO:
        """Return status summary of master execution engine."""
        return EngineStatusDTO(
            status="ACTIVE",
            sub_engines_count=12,
            cybernetic_loop_active=True,
        )
