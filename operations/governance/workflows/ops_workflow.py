"""Operations DTOs module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OperationsPrinciplesDTO:
    """Operations Principles DTO."""

    principle: str = "Zero-Ops Automation"


@dataclass
class OpsWorkflowDTO:
    """Ops Workflow DTO."""

    workflow_id: str = "WF-OPS-01"


@dataclass
class OpsOntologyDTO:
    """Ops Ontology DTO."""

    concept: str = "OperationalExcellence"
