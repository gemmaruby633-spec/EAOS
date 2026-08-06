"""AST Fitness Functions Inspector Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.governance.domain.ast_fitness_models import (
    ASTFitnessReport,
)


@runtime_checkable
class ASTFitnessInspectorPort(Protocol):
    """Port protocol for inspecting AST architecture fitness."""

    async def inspect_repository(self, target_dir: str) -> ASTFitnessReport: ...
