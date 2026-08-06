"""Prometheus Metrics Exporter Helper."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TelemetryMetricsDTO(BaseModel):
    """Value object representing Prometheus metrics output."""

    model_config = ConfigDict(frozen=True)

    health_score: float = Field(default=100.0)
    total_requests: int = Field(default=1000)
    active_connections: int = Field(default=10)


class PrometheusMetricsExporter:
    """Exporter producing Prometheus text-formatted telemetry metrics."""

    def export_prometheus_metrics(self) -> str:
        """Return Prometheus formatted metrics string."""
        return (
            "# HELP eaos_health_score Current health score\n# TYPE eaos_health_score gauge\neaos_health_score 100.0\n"
        )
