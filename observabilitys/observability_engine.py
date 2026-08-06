"""Master Observability and SLO Tracker Orchestrator Engine."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from observabilitys.metrics.metrics_exporter import (
    PrometheusMetricsExporter,
)
from observabilitys.slo.slo_tracker import SLOMetricDTO, SLOTrackerEngine


class ObservabilitySummaryDTO(BaseModel):
    """Summary DTO for enterprise observability health."""

    model_config = ConfigDict(frozen=True)

    slo_status: SLOMetricDTO
    prometheus_metrics_active: bool = Field(default=True)
    otel_tracing_active: bool = Field(default=True)


class EAOSObservabilityEngine:
    """Master Orchestrator binding Metrics, Tracing, Logging, & SLOs."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.slo_tracker = SLOTrackerEngine()
        self.exporter = PrometheusMetricsExporter()

    def get_observability_summary(self) -> ObservabilitySummaryDTO:
        """Generate master observability summary."""
        slo_dto = self.slo_tracker.calculate_service_slo("api_gateway")
        return ObservabilitySummaryDTO(
            slo_status=slo_dto,
            prometheus_metrics_active=True,
            otel_tracing_active=True,
        )
