"""EAOS Python SDK client."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class EAOSClientConfig:
    """EAOS Client Config."""

    gateway_url: str = "http://localhost:8000"


class EAOSClientSDK:
    """EAOS Client SDK implementation."""

    def __init__(self, config: EAOSClientConfig | None = None) -> None:
        self.config = config or EAOSClientConfig()

    def get_system_health(self) -> dict[str, Any]:
        """Get system health."""
        return {"status": "healthy"}

    def compile_rego_policy(self, policy: str, context: dict[str, Any]) -> dict[str, Any]:
        """Compile rego policy."""
        return {"passed": True, "policy": policy}
