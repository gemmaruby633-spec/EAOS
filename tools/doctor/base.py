"""Base Protocol for Plugin Checkers (Enterprise Plugin API)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from tools.doctor.dto import DiagnosticCheckDTO


@runtime_checkable
class BaseChecker(Protocol):
    """Protocol defining the contract for all plugin checkers."""

    checker_id: str
    name: str
    category: str
    version: str
    priority: int
    enabled: bool

    def run(self) -> list[DiagnosticCheckDTO]: ...
