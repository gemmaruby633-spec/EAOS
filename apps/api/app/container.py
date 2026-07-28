"""Re-exporting Composition Root Container for backward compatibility."""

from apps.api.bootstrap.container import (
    policy_evaluator,
    prometheus_exporter,
    topology_use_case,
)

__all__ = [
    "policy_evaluator",
    "prometheus_exporter",
    "topology_use_case",
]
