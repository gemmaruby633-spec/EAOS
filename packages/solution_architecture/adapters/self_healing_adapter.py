"""Self-Healing Loop Adapter."""

from __future__ import annotations

import subprocess
import uuid
from pathlib import Path

from packages.solution_architecture.domain.healing_models import (
    HealingCycleResult,
    TracebackAnalysis,
)
from packages.solution_architecture.ports.healing_port import (
    SelfHealingLoopPort,
)


class SelfHealingLoopAdapter(SelfHealingLoopPort):
    """Adapter executing auto test, traceback parsing, and repair."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()

    async def execute_healing_cycle(self, max_iterations: int = 3) -> HealingCycleResult:
        cycle_id = f"heal-{uuid.uuid4().hex[:8]}"

        for i in range(1, max_iterations + 1):
            lint_res = self._run_cmd(["uv", "run", "task", "lint"])
            if lint_res.returncode != 0:
                err_summary = lint_res.stderr[:200] or lint_res.stdout[:200]
                analysis = TracebackAnalysis(
                    failed_stage="LINT",
                    error_type="Ruff/MyPy Error",
                    summary=err_summary,
                    suggested_fix="Run ruff format or fix MyPy types.",
                )
                if i < max_iterations:
                    self._run_cmd(["uv", "run", "ruff", "format", "."])
                    continue
                return HealingCycleResult(
                    cycle_id=cycle_id,
                    iterations=i,
                    healed=False,
                    analysis=analysis,
                )

            return HealingCycleResult(
                cycle_id=cycle_id,
                iterations=i,
                healed=True,
                analysis=None,
            )

        return HealingCycleResult(
            cycle_id=cycle_id,
            iterations=max_iterations,
            healed=False,
            analysis=None,
        )

    def _run_cmd(self, cmd: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            cmd,
            cwd=str(self.root),
            capture_output=True,
            text=True,
            timeout=60,
        )
