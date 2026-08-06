"""Ops fitness module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OpsFitnessDTO:
    """Ops fitness DTO."""

    score: float = 100.0
