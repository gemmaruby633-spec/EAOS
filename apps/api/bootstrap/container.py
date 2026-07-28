"""Composition Root DI Container assembling all bootstrap modules."""

from apps.api.bootstrap.governance import (
    orchestrator,
    policy_evaluator,
    topology_use_case,
)
from apps.api.bootstrap.telemetry import prometheus_exporter

__all__ = [
    "orchestrator",
    "policy_evaluator",
    "prometheus_exporter",
    "topology_use_case",
]
