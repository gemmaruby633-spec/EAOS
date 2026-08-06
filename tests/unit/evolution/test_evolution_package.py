"""Unit tests for evolution/ package."""

from __future__ import annotations

from evolution.evolution_orchestrator import EAOSEvolutionOrchestrator
from evolution.fitness.fitness_evaluator import ArchitectureFitnessEvaluator


def test_architecture_fitness_evaluator() -> None:
    """Test fitness score evaluation with zero violations."""
    evaluator = ArchitectureFitnessEvaluator()
    fit = evaluator.evaluate_fitness(violations_count=0)

    assert fit.fitness_score == 100.0
    assert fit.is_compliant is True
    assert fit.passed_rules_count == 20


def test_evolution_orchestrator_status() -> None:
    """Test master self-evolution engine status."""
    orchestrator = EAOSEvolutionOrchestrator()
    status = orchestrator.get_evolution_status()

    assert status.maturity_level == "Level 5 - Evolutionary"
    assert status.active_horizons_count == 6
    assert status.evolution_loop_active is True
