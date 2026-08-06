"""Architecture manager."""

from __future__ import annotations

from .decisions.adr_manager import ADRManager


class ArchitectureManager:
    """Architecture manager."""

    def __init__(self) -> None:
        self.adr_manager = ADRManager()
