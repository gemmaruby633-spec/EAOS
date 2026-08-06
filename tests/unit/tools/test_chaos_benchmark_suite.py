"""Unit tests for Swarm & RAG Chaos Engineering & Benchmark Suite."""

from __future__ import annotations

import pytest
from tools.benchmark.swarm_rag_benchmark_adapter import (
    SwarmRAGBenchmarkAdapter,
)
from tools.chaos.dto import ChaosFaultConfig, FaultType
from tools.chaos.swarm_rag_chaos_adapter import SwarmRAGChaosAdapter


@pytest.mark.anyio
async def test_chaos_fault_injection_and_recovery() -> None:
    """Test chaos fault injection on LLM 429 rate limit."""
    adapter = SwarmRAGChaosAdapter()
    cfg = ChaosFaultConfig(
        fault_type=FaultType.LLM_RATE_LIMIT_429,
        target_component="LLMProvider",
    )
    report = await adapter.inject_fault_and_verify(cfg)

    assert report.fallback_triggered is True
    assert report.system_recovered is True
    assert report.recovery_latency_ms >= 0.0


@pytest.mark.anyio
async def test_swarm_rag_performance_benchmark() -> None:
    """Test Swarm & RAG benchmark metrics collection."""
    adapter = SwarmRAGBenchmarkAdapter()
    metrics = await adapter.run_benchmark(iterations=10)

    assert metrics.throughput_ops_sec > 0.0
    assert metrics.p50_latency_ms >= 0.0
    assert metrics.rag_precision_score == 0.98
