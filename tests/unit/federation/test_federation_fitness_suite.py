"""Unit tests for federation/ and fitness/ packages."""

from __future__ import annotations

from federations.federation_engine import EAOSFederationEngine
from fitness.fitness_engine import EAOSFitnessEngine


def test_federation_engine_summary() -> None:
    """Test master federation engine status."""
    engine = EAOSFederationEngine()
    summary = engine.get_federation_summary()

    assert summary.node_id == "node-01"
    assert summary.consensus_protocol == "Synod BFT"
    assert summary.crdt_synced is True


def test_fitness_engine_full_suite() -> None:
    """Test master fitness functions suite evaluation."""
    engine = EAOSFitnessEngine()
    report = engine.evaluate_full_suite()

    assert report.overall_fitness_score == 100.0
    assert report.security_fitness_passed is True
    assert report.architecture_fitness_passed is True
