"""Facade Orchestrator quản lý toàn bộ phân hệ RUNTIME."""

from __future__ import annotations

from typing import Any

from automation.dry_run_runtime_simulator import (
    DryRunRuntimeSimulator,
)
from cache.cache_engine import CacheEngine
from events.event_mesh_engine import EventMeshEngine
from governance.governance_runtime_engine import (
    GovernanceRuntimeEngine,
)
from inventory.inventory_engine import InventoryEngine
from logs.logging_engine import LoggingEngine
from metrics.metrics_engine import MetricsEngine
from models import RuntimeStateSnapshot
from policies.policy_runtime_engine import PolicyRuntimeEngine
from registry.service_registry_engine import (
    ServiceRegistryEngine,
)
from sessions.session_engine import SessionEngine
from state.fsm_state_engine import FsmStateEngine
from traces.quantum_runtime_ledger import QuantumRuntimeLedger
from traces.trace_engine import TraceEngine


class RuntimeManager:
    """Facade hợp nhất điều phối toàn bộ tài nguyên Runtime."""

    def __init__(self) -> None:
        self.cache = CacheEngine()
        self.events = EventMeshEngine()
        self.governance = GovernanceRuntimeEngine()
        self.inventory = InventoryEngine()
        self.logs = LoggingEngine()
        self.metrics = MetricsEngine()
        self.policies = PolicyRuntimeEngine()
        self.registry = ServiceRegistryEngine()
        self.sessions = SessionEngine()
        self.fsm = FsmStateEngine()
        self.traces = TraceEngine()

    def capture_runtime_snapshot(self) -> RuntimeStateSnapshot:
        """Chụp ảnh trạng thái vận hành thời gian thực."""
        sessions_count = self.sessions.get_active_count()
        services_count = len(self.registry.get_all_services())
        hit_ratio = self.cache.get_hit_ratio()

        payload = {
            "sessions": sessions_count,
            "services": services_count,
            "hit_ratio": hit_ratio,
        }
        proof = QuantumRuntimeLedger.generate_trace_proof("RUNTIME-SNAPSHOT", payload)

        return RuntimeStateSnapshot(
            active_sessions=sessions_count,
            active_services=services_count,
            cache_hit_ratio=hit_ratio,
            quantum_proof_hash=proof,
        )

    def simulate_runtime_failover(self, service_id: str) -> dict[str, Any]:
        """Mô phỏng chuyển vùng sự cố dịch vụ."""
        return DryRunRuntimeSimulator.simulate_failover(service_id)
