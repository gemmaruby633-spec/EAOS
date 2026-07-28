"""Unit tests for Governance Domain Entities, Fitness Plugins, and Rules."""

from packages.governance.domain.fitness_metrics import FitnessMetricsCalculator
from packages.governance.domain.fitness_plugins import (
    GenericGovernancePolicyEngine,
    HexagonalBoundaryFitnessRule,
)


def test_hexagonal_boundary_fitness_rule_passes() -> None:
    rule = HexagonalBoundaryFitnessRule()
    clean_imports = [("packages/domain/models.py", "typing")]
    res = rule.evaluate(clean_imports)
    assert res.passed is True
    assert res.violations_count == 0


def test_hexagonal_boundary_fitness_rule_detects_drift() -> None:
    rule = HexagonalBoundaryFitnessRule()
    # Importing 'fastapi' in domain layer correctly triggers violation
    drift_imports = [("packages/domain/models.py", "fastapi")]
    res = rule.evaluate(drift_imports)
    assert res.passed is False
    assert res.violations_count == 1


def test_generic_governance_policy_engine_score_calculation() -> None:
    engine = GenericGovernancePolicyEngine()
    rule = HexagonalBoundaryFitnessRule()
    res = rule.evaluate([("packages/domain/models.py", "fastapi")])

    policy = {
        "base_health_score": 100.0,
        "fitness_rules": {"hexagonal_boundary": {"penalty_per_violation": 10.0}},
    }
    score = engine.calculate_score([res], empty_dirs_count=0, diagnostics_count=0, policy=policy)
    assert score == 90.0


def test_fitness_metrics_calculator() -> None:
    calc = FitnessMetricsCalculator()
    metrics = calc.calculate_metrics(active_files_count=100, import_records=[])
    assert metrics.package_cohesion >= 0.90
    assert metrics.dependency_cycles_count == 0
