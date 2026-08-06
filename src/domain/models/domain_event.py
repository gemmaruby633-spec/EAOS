"""Sự kiện Domain Events cho SecurityPolicy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityPolicyUpdatedEvent:
    """Sự kiện thay đổi chính sách an ninh."""

    policy_id: str
    action: str
    timestamp_ns: int
