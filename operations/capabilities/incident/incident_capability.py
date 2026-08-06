"""Incident Capability module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IncidentCapabilityDTO:
    """Incident capability data transfer object."""

    status: str = "ACTIVE"
    capability_name: str = "IncidentManagement"


IncidentCapability = IncidentCapabilityDTO
