"""Operations Playbooks module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OpsPlaybookDTO:
    """Operations playbook DTO."""

    playbook_id: str = "pb_001"
    title: str = "Disaster Recovery Playbook"
    status: str = "ACTIVE"
