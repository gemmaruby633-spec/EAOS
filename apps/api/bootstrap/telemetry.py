"""Bootstrap module assembling Telemetry Exporter dependencies."""

from apps.api.bootstrap.governance import topology_use_case
from platform_services.telemetry.prometheus_exporter import (
    PrometheusMetricsExporter,
)

prometheus_exporter = PrometheusMetricsExporter(snapshot_provider=topology_use_case.get_audit_report)
