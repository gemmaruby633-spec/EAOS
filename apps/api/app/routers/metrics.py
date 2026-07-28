"""Prometheus Metrics scraping router."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from apps.api.bootstrap.container import prometheus_exporter

router = APIRouter(tags=["Telemetry"])


@router.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    return prometheus_exporter.generate_prometheus_metrics_text()
