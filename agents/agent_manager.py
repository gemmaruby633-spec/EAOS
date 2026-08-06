"""Facade Orchestrator quản lý toàn bộ phân hệ AGENTS."""

from __future__ import annotations

from typing import Any

from .architect.worker import ArchitectWorker
from .automation.dry_run_agent_simulator import DryRunAgentSimulator
from .coder.worker import CoderWorker
from .ledger.quantum_agent_ledger import QuantumAgentLedger
from .models import AgentExecutionResult, AgentRole, AgentTask
from .operator.worker import OperatorWorker
from .planner.worker import PlannerWorker
from .reviewer.worker import ReviewerWorker
from .security.worker import SecurityWorker
from .swarm.swarm_protocol import SwarmProtocol
from .tester.worker import TesterWorker


class AgentManager:
    """Facade hợp nhất điều phối Swarm 7 Agent Workers."""

    def __init__(self) -> None:
        self.architect = ArchitectWorker()
        self.coder = CoderWorker()
        self.operator = OperatorWorker()
        self.planner = PlannerWorker()
        self.reviewer = ReviewerWorker()
        self.security = SecurityWorker()
        self.tester = TesterWorker()
        self.swarm = SwarmProtocol()

    def dispatch_task(self, task: AgentTask) -> AgentExecutionResult:
        """Phân phối task cho Agent Worker thích hợp có đóng dấu."""
        output = f"Dispatched task {task.task_id} to {task.role.value}"
        proof = QuantumAgentLedger.generate_agent_proof(
            task.task_id, {"role": task.role.value, "output": output}
        )
        return AgentExecutionResult(
            task_id=task.task_id,
            success=True,
            output=output,
            proof_hash=proof,
        )

    def simulate_swarm_task(
        self, role: AgentRole, prompt: str
    ) -> dict[str, Any]:
        """Mô phỏng thực thi task của Swarm."""
        return DryRunAgentSimulator.simulate_task(role.value, prompt)
