"""Autonomous Coder Agent Worker."""

from __future__ import annotations

from pathlib import Path

from packages.solution_architecture.adapters.unified_patch_adapter import (
    UnifiedPatchAdapter,
)

from agents.base import AgentRole, AgentWorkResult


class CoderWorker:
    """Worker generating code artifacts and applying patches."""

    role = AgentRole.CODER

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.patch_adapter = UnifiedPatchAdapter(workspace_root=self.root)

    async def execute_work(self, target_file: str, content: str) -> AgentWorkResult:
        res = await self.patch_adapter.apply_patch(target_file, content)
        summary = (
            f"Patch applied to {target_file} (backup saved)." if res.success else f"Patch failed: {res.error_message}"
        )

        return AgentWorkResult(
            agent_role=self.role,
            success=res.success,
            summary=summary,
            details={
                "target_file": target_file,
                "has_backup": res.backup is not None,
            },
        )
