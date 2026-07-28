"""Prometheus native metrics exporter using Pure Dependency Injection."""

from collections.abc import Callable
from packages.governance.domain.ports import AuditSnapshotDTO


class PrometheusMetricsExporter:
    """Exporter generating Prometheus metrics via injected snapshot provider."""

    def __init__(
        self,
        snapshot_provider: Callable[[], AuditSnapshotDTO | None] | None = None,
    ) -> None:
        self._snapshot_provider = snapshot_provider

    def generate_prometheus_metrics_text(self) -> str:
        """Generates Prometheus format metric text. Emits failure flag if snapshot unavailable."""
        snapshot = None
        if self._snapshot_provider is not None:
            try:
                snapshot = self._snapshot_provider()
            except Exception:
                snapshot = None

        # Truthful Observability: Do NOT paint fake 100.0 score if scraping fails!
        if snapshot is None:
            return (
                "# HELP eaos_telemetry_scrape_failed Scraping Failure Flag\n"
                "# TYPE eaos_telemetry_scrape_failed gauge\n"
                "eaos_telemetry_scrape_failed 1.0\n"
                "# HELP eaos_architecture_health_score System Health Score\n"
                "# TYPE eaos_architecture_health_score gauge\n"
                "eaos_architecture_health_score 0.0\n"
            )

        return (
            f"# HELP eaos_telemetry_scrape_failed Scraping Failure Flag\n"
            f"# TYPE eaos_telemetry_scrape_failed gauge\n"
            f"eaos_telemetry_scrape_failed 0.0\n"
            f"# HELP eaos_architecture_health_score System Health Score\n"
            f"# TYPE eaos_architecture_health_score gauge\n"
            f"eaos_architecture_health_score {snapshot.calculated_health_score:.1f}\n"
            f"# HELP eaos_active_source_files Total Active Source Files\n"
            f"# TYPE eaos_active_source_files gauge\n"
            f"eaos_active_source_files {snapshot.active_source_files}\n"
            f"# HELP eaos_coupling_index Coupling Index\n"
            f"# TYPE eaos_coupling_index gauge\n"
            f"eaos_coupling_index {snapshot.coupling_index:.3f}\n"
            f"# HELP eaos_instability_index Instability Index\n"
            f"# TYPE eaos_instability_index gauge\n"
            f"eaos_instability_index {snapshot.instability_index:.3f}\n"
            f"# HELP eaos_package_cohesion Package Cohesion Score\n"
            f"# TYPE eaos_package_cohesion gauge\n"
            f"eaos_package_cohesion {snapshot.package_cohesion:.2f}\n"
        )
