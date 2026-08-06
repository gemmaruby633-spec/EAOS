"""Ops simulation module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OpsSimulationDTO:
    """Ops simulation DTO."""

    status: str = "SIMULATED_PASS"
