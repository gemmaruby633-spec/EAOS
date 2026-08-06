from typing import Protocol

from tools.doctor.dto import DiagnosticCheckDTO


class BaseChecker(Protocol):
    """Protocol for doctor checkers used by registry and engine."""

    checker_id: str
    enabled: bool

    def run(self) -> list[DiagnosticCheckDTO]: ...
