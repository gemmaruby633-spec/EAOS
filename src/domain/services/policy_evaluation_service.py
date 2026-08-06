"""Domain Service đánh giá tuân thủ chính sách."""

from __future__ import annotations

from domain.models.security_policy import PolicyAction, SecurityPolicy


class PolicyEvaluationService:
    """Service kiểm tra tuân thủ chính sách."""

    @staticmethod
    def is_access_granted(policy: SecurityPolicy, resource: str) -> bool:
        """Kiểm tra quyền truy cập."""
        if not policy.is_active:
            return False
        action = policy.evaluate_resource(resource)
        return action == PolicyAction.ALLOW
