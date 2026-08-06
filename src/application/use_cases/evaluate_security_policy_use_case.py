"""Use Case thực thi đánh giá chính sách an ninh."""

from __future__ import annotations

from typing import Any

from application.ports.security_policy_repository import (
    SecurityPolicyRepository,
)
from domain.services.policy_evaluation_service import (
    PolicyEvaluationService,
)


class EvaluateSecurityPolicyUseCase:
    """Use Case kiểm tra quyền truy cập tài nguyên."""

    def __init__(self, repo: SecurityPolicyRepository) -> None:
        self.repo = repo

    def execute(self, policy_id: str, resource: str) -> dict[str, Any]:
        """Thực thi đánh giá."""
        policy = self.repo.get_by_id(policy_id)
        if not policy:
            return {"granted": False, "reason": "POLICY_NOT_FOUND"}

        granted = PolicyEvaluationService.is_access_granted(policy, resource)
        return {"granted": granted, "reason": "EVALUATED"}
