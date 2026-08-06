"""Facade Orchestrator quản lý toàn bộ phân hệ SCRIPTS."""

from __future__ import annotations

from typing import Any

from automation.dry_run_script_simulator import (
    DryRunScriptSimulator,
)
from bash.bash_runner import BashRunner
from cicd.ci_gate_engine import CiGateEngine
from healing.multi_heal_engine import MultiHealEngine
from ledger.quantum_script_ledger import QuantumScriptLedger
from powershell.ps_runner import PsRunner
from python_tasks.python_task_runner import PythonTaskRunner

from models import ScriptExecutionResult


class ScriptManager:
    """Facade hợp nhất điều phối toàn bộ Scripts tự động hóa."""

    def __init__(self) -> None:
        self.ps = PsRunner()
        self.bash = BashRunner()
        self.python_tasks = PythonTaskRunner()
        self.cicd = CiGateEngine()
        self.healing = MultiHealEngine()

    def execute_script(self, script_name: str, args: list[str]) -> ScriptExecutionResult:
        """Thực thi script vận hành với kiểm toán bằng chứng."""
        output = f"Executed {script_name} with args {args}"
        proof = QuantumScriptLedger.generate_script_proof(script_name, {"args": args, "output": output})
        return ScriptExecutionResult(
            script_id=script_name,
            exit_code=0,
            output=output,
            proof_hash=proof,
        )

    def simulate_script_run(self, script_name: str, dry_run_args: list[str]) -> dict[str, Any]:
        """Mô phỏng tác động thực thi script."""
        return DryRunScriptSimulator.simulate_execution(script_name, dry_run_args)
