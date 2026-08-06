"""OpenTelemetry exporter factories for OTLP gRPC and HTTP."""

from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)


def create_otlp_http_exporter(
    endpoint: str = "http://localhost:4318/v1/traces",
) -> OTLPSpanExporter:
    """Factory creating an OTLP HTTP span exporter for Collector."""
    return OTLPSpanExporter(endpoint=endpoint)
