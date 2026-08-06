"""Decision Table Evaluator (DMN Standard)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from decisions.rules.rule_evaluator import (
    DecisionRuleDTO,
    DecisionRuleEvaluator,
)


class DecisionResultDTO(BaseModel):
    """Result produced by decision table evaluation."""

    model_config = ConfigDict(frozen=True)

    decision_id: str
    matched_rule_id: str | None = Field(default=None)
    outcome: str = Field(default="DEFAULT_REJECT")
    passed: bool = Field(default=False)


class DecisionTableEvaluator:
    """Evaluator executing DMN Decision Tables."""

    def __init__(self) -> None:
        self.rule_evaluator = DecisionRuleEvaluator()

    def evaluate_table(
        self,
        decision_id: str,
        rules: list[DecisionRuleDTO],
        context: dict[str, Any],
    ) -> DecisionResultDTO:
        """Evaluate list of decision rules sequentially."""
        for rule in rules:
            if self.rule_evaluator.evaluate_rule(rule, context):
                return DecisionResultDTO(
                    decision_id=decision_id,
                    matched_rule_id=rule.rule_id,
                    outcome=rule.outcome,
                    passed=True,
                )

        return DecisionResultDTO(
            decision_id=decision_id,
            matched_rule_id=None,
            outcome="DEFAULT_REJECT",
            passed=False,
        )
