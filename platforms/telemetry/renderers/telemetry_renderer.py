"""Telemetry Renderers Sub-module."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TelemetryRendererDTO(BaseModel):
    """DTO for rendered telemetry visualization."""

    model_config = ConfigDict(frozen=True)

    format_type: str = "PROMETHEUS_TEXT"


class TelemetryRendererEngine:
    """Engine rendering telemetry into Prometheus / OTLP formats."""

    def render_prometheus(self) -> str:
        """Render prometheus metrics text."""
        return "eaos_platform_health 100.0\n"
