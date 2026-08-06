"""Triển khai InMemory cho SecurityPolicyRepository."""

from __future__ import annotations

from domain.models.security_policy import (
    PolicyAction,
    SecurityPolicy,
    SecurityRule,
)


class InMemoryPolicyRepository:
    """Repository lưu trữ chính sách trong bộ nhớ."""

    def __init__(self) -> None:
        self._policies: dict[str, SecurityPolicy] = {}

        default_policy = SecurityPolicy("POL-01", "Default Access")
        default_policy.add_rule(SecurityRule("R-1", "/v1/api", PolicyAction.ALLOW))
        self._policies["POL-01"] = default_policy

    def get_by_id(self, policy_id: str) -> SecurityPolicy | None:
        """Lấy chính sách theo ID."""
        return self._policies.get(policy_id)

    def save(self, policy: SecurityPolicy) -> None:
        """Lưu chính sách."""
        self._policies[policy.policy_id] = policy
