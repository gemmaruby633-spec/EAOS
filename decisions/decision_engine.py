"""Master Enterprise Decision Engine Orchestrator."""

from __future__ import annotations

from typing import Any

from decisions.evaluation.decision_table_evaluator import (
    DecisionResultDTO,
    DecisionTableEvaluator,
)
from decisions.optimization.decision_optimizer import (
    DecisionOptimizer,
    OptimizationResultDTO,
)
from decisions.planning.scenario_decision_planner import (
    ScenarioDecisionPlanner,
)
from decisions.rules.rule_evaluator import (
    DecisionRuleDTO,
)


class EnterpriseDecisionEngine:
    """Master Orchestrator for Rules, DMN Tables, Planning & Optimization."""

    def __init__(self) -> None:
        self.table_evaluator = DecisionTableEvaluator()
        self.planner = ScenarioDecisionPlanner()
        self.optimizer = DecisionOptimizer()

    def execute_enterprise_decision(
        self,
        decision_id: str,
        rules: list[DecisionRuleDTO],
        context: dict[str, Any],
    ) -> tuple[DecisionResultDTO, OptimizationResultDTO]:
        """Execute decision evaluation and utility optimization."""
        eval_result = self.table_evaluator.evaluate_table(decision_id, rules, context)
        opt_result = self.optimizer.optimize_decision(decision_id)
        return eval_result, opt_result
