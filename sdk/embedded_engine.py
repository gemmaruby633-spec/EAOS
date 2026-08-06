"""SDK embedded engine module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class EmbeddedResultDTO:
    """Embedded result DTO."""

    in_process: bool = True
    domain: str = ""
    action: str = ""


class EAOSEmbeddedEngine:
    """EAOS Embedded engine."""

    def __init__(self, config: Any = None) -> None:
        self.config = config

    def initialize(self) -> bool:
        """Initialize embedded engine."""
        return True

    def execute_in_process(self, domain: str = "", action: str = "") -> EmbeddedResultDTO:
        """Execute action in process."""
        return EmbeddedResultDTO(in_process=True, domain=domain, action=action)


EmbeddedEngine = EAOSEmbeddedEngine
