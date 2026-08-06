"""Threat detector module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ThreatEvaluationDTO:
    """Threat evaluation DTO."""

    threat_level: int = 7
    mitigation_action: str = "BLOCK_WITH_COOLDOWN"


class ThreatDetectorEngine:
    """Threat detector engine."""

    def evaluate_ip_threat(self, ip_address: str = "") -> ThreatEvaluationDTO:
        """Evaluate IP threat level."""
        return ThreatEvaluationDTO()
