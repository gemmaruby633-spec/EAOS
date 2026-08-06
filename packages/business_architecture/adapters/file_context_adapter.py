"""File Context Engine Adapter."""

from __future__ import annotations

from pathlib import Path

from packages.business_architecture.domain.context_models import (
    InjectedPromptContext,
    SystemContextPayload,
)
from packages.business_architecture.ports.context_engine_port import (
    ContextEnginePort,
)


class FileContextAdapter(ContextEnginePort):
    """Adapter reading Constitution, ADRs, and pyproject.toml."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()

    async def build_system_context(self) -> SystemContextPayload:
        constitution = self._read_file("ARCHITECTURE_CONSTITUTION.md")
        pyproject = self._read_file("pyproject.toml")
        adrs = self._load_adrs()

        return SystemContextPayload(
            constitution_text=constitution[:1500],
            adr_summaries=adrs,
            pyproject_specs=pyproject[:1000],
            active_capability="cap-control-room",
        )

    async def inject_context_into_prompt(self, user_prompt: str) -> InjectedPromptContext:
        payload = await self.build_system_context()

        adr_block = "\n".join(f"- {a}" for a in payload.adr_summaries)
        formatted = (
            "=== EAOS ENTERPRISE CONSTITUTION CONTEXT ===\n"
            f"{payload.constitution_text}\n\n"
            "=== KEY ADRs ===\n"
            f"{adr_block}\n\n"
            "=== USER INSTRUCTION ===\n"
            f"{user_prompt}"
        )

        return InjectedPromptContext(
            user_prompt=user_prompt,
            context_payload=payload,
            formatted_prompt=formatted,
        )

    def _read_file(self, fname: str) -> str:
        target = self.root / fname
        if target.exists():
            return target.read_text(encoding="utf-8")
        return ""

    def _load_adrs(self) -> list[str]:
        adr_dir = self.root / "docs" / "adr"
        if not adr_dir.exists():
            return ["ADR-UI-001: EAOS Interaction Architecture (RATIFIED)"]

        summaries = []
        for f in sorted(adr_dir.glob("*.md")):
            lines = f.read_text(encoding="utf-8").splitlines()
            title = lines[0] if lines else f.name
            summaries.append(title.strip("# "))
        return summaries or ["ADR-UI-001: EAOS Interaction Architecture (RATIFIED)"]
