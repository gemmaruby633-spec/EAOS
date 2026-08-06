"""Ops Metrics Module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class OpsMetricsDTO(BaseModel):
    """DTO for Ops Metrics."""

    model_config = ConfigDict(frozen=True)

    metric_name: str = "ops_latency"
