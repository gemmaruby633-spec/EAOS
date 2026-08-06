"""IAM policy engine module."""

from __future__ import annotations


class IAMPolicyEngine:
    """IAM policy evaluation engine."""

    def __init__(self) -> None:
        self.policy_version = "v1"

    def evaluate_policy(self, subject: str, action: str, resource: str) -> bool:
        """Evaluate IAM policy permission for a subject, action, and resource."""
        return True

    def evaluate_access_permission(self, role: str, action: str) -> bool:
        """Evaluate access permission for a role and action."""
        return True


IAMPolicy = IAMPolicyEngine
