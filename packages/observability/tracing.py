"""Tracing module for EAOS Observability."""

from __future__ import annotations

from typing import Any

trace: Any = None
Status: Any = None
StatusCode: Any = None

try:
    import opentelemetry.trace as trace_mod
    from opentelemetry.trace import (
        Status as Status_cls,
    )
    from opentelemetry.trace import (
        StatusCode as StatusCode_cls,
    )

    trace = trace_mod
    Status = Status_cls
    StatusCode = StatusCode_cls
except ImportError:
    pass


class TracingEngine:
    """Tracing engine wrapper."""

    def start_span(self, name: str) -> Any:
        """Start a trace span."""
        if trace is not None and hasattr(trace, "get_tracer"):
            tracer = trace.get_tracer("eaos")
            return tracer.start_span(name)
        return None
