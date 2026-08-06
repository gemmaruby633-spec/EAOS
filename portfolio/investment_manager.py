"""Lớp Facade trung tâm duy trì tính Tương thích ngược 100%."""

from __future__ import annotations

from typing import Any

from automation.dry_run_simulator import DryRunSimulator
from epics.epic_engine import EpicEngine
from epics.models import WSJFScore
from initiatives.initiative_engine import InitiativeEngine
from investment.valuation_engine import ValuationEngine
from programs.program_engine import ProgramEngine
from projects.project_engine import ProjectEngine


class InvestmentManager:
    """Facade hợp nhất điều phối toàn bộ phân hệ PORTFOLIO."""

    def __init__(self) -> None:
        self.epic_engine = EpicEngine()
        self.initiative_engine = InitiativeEngine()
        self.valuation_engine = ValuationEngine()
        self.program_engine = ProgramEngine()
        self.project_engine = ProjectEngine()

    def evaluate_investment_proposal(
        self,
        base_investment: float,
        cash_flows: list[float],
    ) -> dict[str, Any]:
        """Đánh giá đề xuất đầu tư bằng Monte Carlo và mã hóa."""
        val = self.valuation_engine.run_monte_carlo_valuation(base_investment, cash_flows)
        return {
            "NPV": val.npv,
            "OptionValue": val.option_value,
            "EvidenceProof": val.quantum_evidence_hash,
        }

    def register_and_score_epic(
        self,
        epic_id: str,
        title: str,
        owner: str,
        user_val: float,
        time_crit: float,
        rroe: float,
        job_size: float,
    ) -> float:
        """Đăng ký Epic và trả về điểm số WSJF."""
        wsjf = WSJFScore(
            user_value=user_val,
            time_criticality=time_crit,
            rroe=rroe,
            job_size=job_size,
        )
        epic = self.epic_engine.register_epic(epic_id, title, owner, wsjf)
        return epic.wsjf.score

    def simulate_reallocation(
        self,
        current: dict[str, float],
        delta: dict[str, float],
    ) -> dict[str, Any]:
        """Thực hiện mô phỏng chuyển ngân sách an toàn."""
        return DryRunSimulator.simulate_budget_reallocation(current, delta)
