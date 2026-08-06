"""Registry managing diagnostic checkers (Open/Closed Principle)."""

from __future__ import annotations

from pathlib import Path

from tools.doctor.checkers.ai_checker import AIChecker
from tools.doctor.checkers.base import BaseChecker
from tools.doctor.checkers.docker_checker import DockerChecker
from tools.doctor.checkers.filesystem_checker import FilesystemChecker
from tools.doctor.checkers.governance_checker import GovernanceChecker
from tools.doctor.checkers.infrastructure_checker import (
    InfrastructureChecker,
)
from tools.doctor.checkers.observability_checker import (
    ObservabilityChecker,
)
from tools.doctor.checkers.package_checker import PackageChecker
from tools.doctor.checkers.runtime_checker import RuntimeChecker
from tools.doctor.checkers.security_checker import SecurityChecker
from tools.doctor.checkers.smoke_checker import SmokeChecker
from tools.doctor.checkers.validator_checker import ValidatorChecker
from tools.doctor.checkers.workspace_checker import WorkspaceChecker


class CheckerRegistry:
    """Registry providing extensible diagnostic checkers."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self._checkers: list[BaseChecker] = []
        self._register_default_checkers()

    def _register_default_checkers(self) -> None:
        self.register(RuntimeChecker())
        self.register(WorkspaceChecker(self.root))
        self.register(FilesystemChecker(self.root))
        self.register(PackageChecker(self.root))
        self.register(InfrastructureChecker())
        self.register(DockerChecker())
        self.register(ObservabilityChecker())
        self.register(GovernanceChecker(self.root))
        self.register(ValidatorChecker(self.root))
        self.register(AIChecker())
        self.register(SecurityChecker(self.root))
        self.register(SmokeChecker(self.root))

    def register(self, checker: BaseChecker) -> None:
        """Register a new diagnostic checker."""
        self._checkers.append(checker)

    def get_checkers(self) -> list[BaseChecker]:
        """Return list of configured diagnostic checkers."""
        return self._checkers
