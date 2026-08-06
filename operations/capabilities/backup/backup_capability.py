"""Backup Capability Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BackupCapabilityDTO(BaseModel):
    """DTO for Backup Capability."""

    model_config = ConfigDict(frozen=True)

    status: str = "ACTIVE"
