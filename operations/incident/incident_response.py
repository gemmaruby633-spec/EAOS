"""Incident Response P1-P4 Management Engine."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class IncidentSeverity(StrEnum):
    """Incident severity classification P1 to P4."""

    P1_CRITICAL = "P1_CRITICAL"
    P2_MAJOR = "P2_MAJOR"
    P3_MINOR = "P3_MINOR"
    P4_ADVISORY = "P4_ADVISORY"


class IncidentTicketDTO(BaseModel):
    """Value object representing an operational incident ticket."""

    model_config = ConfigDict(frozen=True)

    ticket_id: str = Field(..., description="Ticket ID e.g. INC-001")
    summary: str = Field(..., description="Incident summary")
    severity: IncidentSeverity = Field(default=IncidentSeverity.P3_MINOR)
    is_resolved: bool = Field(default=True)


class IncidentResponseEngine:
    """Engine managing P1-P4 operational incident triage."""

    def create_incident_ticket(self, summary: str, severity: IncidentSeverity) -> IncidentTicketDTO:
        """Create and log operational incident ticket."""
        return IncidentTicketDTO(
            ticket_id="INC-OPS-001",
            summary=summary,
            severity=severity,
            is_resolved=True,
        )
