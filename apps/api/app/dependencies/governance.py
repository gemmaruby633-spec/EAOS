"""FastAPI Dependency Injection providers for Governance Capability."""

from typing import Any
from apps.api.bootstrap.container import (
    policy_evaluator,
    prometheus_exporter,
    topology_use_case,
)


def get_topology_use_case() -> Any:
    return topology_use_case


def get_prometheus_exporter() -> Any:
    return prometheus_exporter


def get_policy_evaluator() -> Any:
    return policy_evaluator
