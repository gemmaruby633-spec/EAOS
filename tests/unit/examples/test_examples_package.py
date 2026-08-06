"""Unit tests for examples/ package."""

from __future__ import annotations

from examples.runner import EAOSExamplesRunner


def test_eaos_examples_runner_execution() -> None:
    """Test executing master EAOS examples runner."""
    runner = EAOSExamplesRunner()
    summary = runner.run_all_examples()

    assert summary.total_examples_run == 5
    assert summary.all_passed is True
