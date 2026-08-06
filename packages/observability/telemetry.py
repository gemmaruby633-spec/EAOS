"""Telemetry module for EAOS Observability."""

from __future__ import annotations

from typing import Any

trace: Any = None
try:
    import opentelemetry.trace as trace_mod

    trace = trace_mod
except ImportError:
    pass


class TelemetryEngine:
    """Telemetry engine wrapper."""

    def get_tracer(self) -> Any:
        """Get tracer instance."""
        if trace is not None and hasattr(trace, "get_tracer"):
            return trace.get_tracer("eaos")
        return None
