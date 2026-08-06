"""SDK manager module."""

from __future__ import annotations

from .embedded.embedded_runner import EmbeddedRunner
from .ledger.quantum_sdk_ledger import QuantumSdkLedger


class SdkManager:
    """SDK manager."""

    def __init__(self) -> None:
        self.runner = EmbeddedRunner()
        self.ledger = QuantumSdkLedger()
