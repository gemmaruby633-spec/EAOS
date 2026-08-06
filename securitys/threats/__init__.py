"""Security threats package."""

from __future__ import annotations

from .threat_detector import ThreatDetectorEngine

ThreatDetector = ThreatDetectorEngine

__all__ = ["ThreatDetector", "ThreatDetectorEngine"]
