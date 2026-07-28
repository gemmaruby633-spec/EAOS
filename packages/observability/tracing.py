"""Business capability tracer for enterprise observability spans."""

from typing import Any
from opentelemetry import trace  # type: ignore[import-not-found]
from opentelemetry.trace import Status, StatusCode  # type: ignore[import-not-found]


class BusinessCapabilityTracer:
    """Traces execution spans tagged with business capability metadata."""

    def __init__(self, tracer_name: str = "eaos.capability") -> None:
        self._tracer = trace.get_tracer(tracer_name)

    def trace_capability_execution(
        self,
        capability_id: str,
        action: str,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        """Executes action within a capability-attributed tracing span."""
        span_name = f"Capability:{capability_id}/{action}"
        with self._tracer.start_as_current_span(span_name) as span:
            span.set_attribute("enterprise.capability_id", capability_id)
            span.set_attribute("enterprise.action", action)
            if metadata:
                for k, v in metadata.items():
                    span.set_attribute(f"enterprise.metadata.{k}", str(v))
            span.set_status(Status(StatusCode.OK))
            return True
