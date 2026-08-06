"""Recovery Capability module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RecoveryCapabilityDTO:
    """Recovery capability data transfer object."""

    status: str = "ACTIVE"


RecoveryCapability = RecoveryCapabilityDTO
