"""OpenTelemetry SDK lifecycle manager for EAOS."""

from opentelemetry import trace  # type: ignore[import-not-found]
from opentelemetry.sdk.trace import TracerProvider  # type: ignore[import-not-found]
from opentelemetry.sdk.trace.export import BatchSpanProcessor  # type: ignore[import-not-found]
from packages.observability.exporters import create_otlp_http_exporter
from packages.observability.resource import create_eaos_resource


def setup_telemetry(
    service_name: str = "eaos-core",
    otlp_endpoint: str = "http://localhost:4318/v1/traces",
) -> None:
    """Configures global TracerProvider with BatchSpanProcessor and OTLP Exporter."""
    resource = create_eaos_resource(service_name=service_name)
    provider = TracerProvider(resource=resource)
    exporter = create_otlp_http_exporter(endpoint=otlp_endpoint)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
