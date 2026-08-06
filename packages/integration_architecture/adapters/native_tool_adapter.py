"""Native Tool Calling Adapter."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import ClassVar

from packages.integration_architecture.domain.tool_models import (
    ToolExecutionRequest,
    ToolExecutionResult,
)
from packages.integration_architecture.ports.tool_calling_port import (
    NativeToolCallingPort,
)


class NativeToolCallingAdapter(NativeToolCallingPort):
    """Adapter executing CLI tools and filesystem operations."""

    ALLOWED_CLI: ClassVar[frozenset[str]] = frozenset({"uv", "pytest", "ruff", "mypy", "git", "docker"})

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()

    def list_available_tools(self) -> list[str]:
        return [
            "read_file",
            "list_dir",
            "grep_search",
            "run_ruff",
            "run_pytest",
            "git_status",
            "docker_ps",
        ]

    async def execute_tool(self, request: ToolExecutionRequest) -> ToolExecutionResult:
        name = request.tool_name
        args = request.arguments

        try:
            if name == "read_file":
                out = self._read_file(args.get("path", ""))
            elif name == "list_dir":
                out = self._list_dir(args.get("path", "."))
            elif name == "grep_search":
                out = self._grep_search(args.get("pattern", ""), args.get("path", "."))
            elif name == "run_ruff":
                out = self._run_cli(["uv", "run", "task", "lint"])
            elif name == "run_pytest":
                out = self._run_cli(["uv", "run", "task", "test"])
            elif name == "git_status":
                out = self._run_cli(["git", "status", "--short"])
            elif name == "docker_ps":
                out = self._run_cli(["docker", "ps", "--format", "table"])
            else:
                return ToolExecutionResult(
                    success=False,
                    tool_name=name,
                    error=f"Tool '{name}' is unknown or disallowed.",
                )

            return ToolExecutionResult(success=True, tool_name=name, output=out)
        except Exception as err:
            return ToolExecutionResult(success=False, tool_name=name, error=str(err))

    def _read_file(self, rel_path: str) -> str:
        target = (self.root / rel_path).resolve()
        target.relative_to(self.root)
        if not target.exists():
            return f"Error: File '{rel_path}' does not exist."
        return target.read_text(encoding="utf-8")

    def _list_dir(self, rel_path: str) -> str:
        target = (self.root / rel_path).resolve()
        target.relative_to(self.root)
        if not target.exists():
            return f"Error: Directory '{rel_path}' not found."
        items = [f.name + ("/" if f.is_dir() else "") for f in target.iterdir()]
        return "\n".join(sorted(items)[:100])

    def _grep_search(self, pattern: str, rel_path: str) -> str:
        target = (self.root / rel_path).resolve()
        target.relative_to(self.root)
        matches = []
        files = [target] if target.is_file() else list(target.rglob("*.py"))[:50]

        for f in files:
            try:
                lines = f.read_text(encoding="utf-8").splitlines()
                for idx, line in enumerate(lines, start=1):
                    if pattern in line:
                        rel = f.relative_to(self.root)
                        matches.append(f"{rel}:{idx}:{line.strip()}")
            except Exception:
                continue
        return "\n".join(matches[:30]) or "No matches found."

    def _run_cli(self, cmd: list[str]) -> str:
        if not cmd or cmd[0] not in self.ALLOWED_CLI:
            return "Command execution blocked by security policy."
        try:
            res = subprocess.run(
                cmd,
                cwd=str(self.root),
                capture_output=True,
                text=True,
                timeout=90,
            )
            return res.stdout or res.stderr
        except subprocess.TimeoutExpired:
            return "CLI execution timed out after 90 seconds."
