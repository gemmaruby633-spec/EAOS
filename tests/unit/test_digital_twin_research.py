"""Unit tests for Digital Twin Counterfactual Research Engine."""

from packages.simulation.application.use_cases import RunCounterfactualResearchUseCase
from packages.simulation.infrastructure.adapters import (
    InMemoryDigitalTwinSandboxAdapter,
    InMemoryResearchReportRepository,
)


def test_counterfactual_research_experiment_flow() -> None:
    sandbox_adapter = InMemoryDigitalTwinSandboxAdapter()
    report_repo = InMemoryResearchReportRepository()
    use_case = RunCounterfactualResearchUseCase(sandbox_adapter, report_repo)

    base_state = {
        "version": "1.0.0",
        "cache_strategy": "STANDARD_SPLAY",
        "db_max_connections": 20,
    }

    beta_mutation = {
        "simulated_delay_ms": 10.0,
        "simulated_fitness": 0.96,
        "simulated_memory_mb": 38.0,
        "simulated_errors": 0,
    }

    workload = {
        "task_count": 500,
        "concurrent_users": 50,
        "target_endpoint": "/v1/knowledge/query",
    }

    report = use_case.execute_experiment(
        experiment_name="EXP-2026-SPLAY-OPTIMIZATION",
        base_state=base_state,
        beta_mutation=beta_mutation,
        workload_payload=workload,
    )

    assert report.report_id.startswith("RPT-")
    assert report.experiment_name == "EXP-2026-SPLAY-OPTIMIZATION"
    assert report.fitness_delta_pct > 0
    assert "KHUYẾN NGHỊ ÁP DỤNG" in report.overall_recommendation

    assert len(report.deltas) == 3
    
    fit_delta = next(d for d in report.deltas if d.metric_name == "Architecture Fitness Score")
    assert fit_delta.is_improvement is True
    assert fit_delta.beta_value == 0.96
    assert fit_delta.alpha_value == 0.82

    saved_report = report_repo.find_report_by_id(report.report_id)
    assert saved_report is not None
    assert saved_report.report_id == report.report_id
