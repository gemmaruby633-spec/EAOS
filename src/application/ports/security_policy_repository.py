"""Abstract Port cho Repository lưu trữ chính sách."""

from __future__ import annotations

from typing import Protocol

from domain.models.security_policy import SecurityPolicy


class SecurityPolicyRepository(Protocol):
    """Giao diện Port lưu trữ SecurityPolicy."""

    def get_by_id(self, policy_id: str) -> SecurityPolicy | None:
        """Lấy chính sách theo ID."""
        ...

    def save(self, policy: SecurityPolicy) -> None:
        """Lưu chính sách."""
        ...
