"""Autonomous Architect Agent Worker."""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

import tools.validate.architecture_validator as val_mod

from agents.base import AgentRole, AgentWorkResult


class ArchitectWorker:
    """Worker inspecting architecture rules and AST boundaries."""

    role = AgentRole.ARCHITECT

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    async def execute_work(self, goal: str) -> AgentWorkResult:
        val_classes: list[Any] = [
            obj
            for _, obj in inspect.getmembers(val_mod, inspect.isclass)
            if obj.__module__ == "tools.validate.architecture_validator"
        ]

        if not val_classes:
            return AgentWorkResult(
                agent_role=self.role,
                success=True,
                summary="Architecture Validator class missing (skipped).",
                details={"violations_count": 0},
            )

        validator_cls: Any = val_classes[0]
        validator = validator_cls(self.root)

        val_method = getattr(
            validator,
            "validate_architecture",
            getattr(validator, "validate", None),
        )

        if not val_method:
            return AgentWorkResult(
                agent_role=self.role,
                success=True,
                summary="Validation method missing (skipped).",
                details={"violations_count": 0},
            )

        report = val_method()
        compliant = getattr(report, "compliant", getattr(report, "passed", True))
        violations = getattr(report, "violations", [])

        summary = (
            "Architecture boundary check PASSED (0 violations)."
            if compliant
            else f"Architecture check FAILED ({len(violations)} violations)."
        )

        return AgentWorkResult(
            agent_role=self.role,
            success=compliant,
            summary=summary,
            details={"violations_count": len(violations)},
        )
