"""Monitoring Capability module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MonitoringCapabilityDTO:
    """Monitoring capability data transfer object."""

    status: str = "ACTIVE"


MonitoringCapability = MonitoringCapabilityDTO
