"""Mô hình Domain Aggregate SecurityPolicy."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class PolicyAction(StrEnum):
    """Hành động kiểm soát chính sách."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    AUDIT = "AUDIT"


@dataclass(frozen=True)
class SecurityRule:
    """Quy tắc an ninh thuộc SecurityPolicy."""

    rule_id: str
    resource: str
    action: PolicyAction


@dataclass
class SecurityPolicy:
    """Aggregate Root đại diện cho Chính sách An ninh."""

    policy_id: str
    name: str
    is_active: bool = True
    rules: list[SecurityRule] = field(default_factory=list)

    def add_rule(self, rule: SecurityRule) -> None:
        """Thêm quy tắc mới vào chính sách."""
        self.rules.append(rule)

    def evaluate_resource(self, resource: str) -> PolicyAction:
        """Kiểm tra hành động cho tài nguyên."""
        for rule in self.rules:
            if rule.resource == resource or rule.resource == "*":
                return rule.action
        return PolicyAction.DENY
