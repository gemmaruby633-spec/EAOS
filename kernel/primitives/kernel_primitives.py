"""Core Immutable Value Objects and Primitives for Frozen Kernel."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class KernelEntityID(BaseModel):
    """Value object representing an immutable Kernel Entity ID."""

    model_config = ConfigDict(frozen=True)

    value: str = Field(default_factory=lambda: f"kernel-{uuid.uuid4().hex[:8]}")


class KernelTimestamp(BaseModel):
    """Value object representing UTC timestamp in Frozen Kernel."""

    model_config = ConfigDict(frozen=True)

    utc_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
