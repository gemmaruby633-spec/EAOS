"""Unit tests for decisions/ package."""

from __future__ import annotations

from decisions.decision_engine import EnterpriseDecisionEngine
from decisions.rules.rule_evaluator import (
    DecisionRuleDTO,
    RuleConditionDTO,
)


def test_enterprise_decision_engine_execution() -> None:
    """Test executing enterprise decision rules and optimization."""
    engine = EnterpriseDecisionEngine()

    rule1 = DecisionRuleDTO(
        rule_id="R01",
        name="Expense Approval",
        conditions=[RuleConditionDTO(field="amount", operator="<", value=1000000)],
        outcome="AUTO_APPROVE",
    )

    context = {"amount": 500000}
    eval_res, opt_res = engine.execute_enterprise_decision("DEC-EXP-001", [rule1], context)

    assert eval_res.passed is True
    assert eval_res.matched_rule_id == "R01"
    assert eval_res.outcome == "AUTO_APPROVE"
    assert opt_res.optimized_utility_score > 0.0
