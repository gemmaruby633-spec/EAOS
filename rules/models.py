"""Mô hình DTO cho hệ thống Quy tắc Doanh nghiệp (RULES)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class RuleSeverity(StrEnum):
    """Mức độ nghiêm trọng của vi phạm quy tắc."""

    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    BLOCKER = "BLOCKER"


@dataclass(frozen=True)
class RuleDefinition:
    """Định nghĩa quy tắc quản trị."""

    rule_id: str
    name: str
    category: str
    severity: RuleSeverity
    description: str


@dataclass
class EvaluationResult:
    """Kết quả đánh giá quy tắc."""

    rule_id: str
    passed: bool
    message: str
    context: dict[str, str] = field(default_factory=dict)
