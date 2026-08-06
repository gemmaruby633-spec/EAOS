"""Telemetry Collectors Sub-module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TelemetryCollectorDTO(BaseModel):
    """Value object for telemetry collection."""

    model_config = ConfigDict(frozen=True)

    collector_name: str = "otlp_collector"
    metrics_buffered_count: int = Field(default=100)


class TelemetryCollectorEngine:
    """Engine collecting platform metrics and trace spans."""

    def collect_metrics(self) -> TelemetryCollectorDTO:
        """Collect telemetry metrics snapshot."""
        return TelemetryCollectorDTO(collector_name="otlp_collector", metrics_buffered_count=100)
