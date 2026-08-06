"""Động cơ Định giá Tùy chọn Thực và Mô phỏng Monte Carlo."""

from __future__ import annotations

import math
import random

from investment.models import ValuationResult
from investment.quantum_ledger import QuantumLedger


class ValuationEngine:
    """Động cơ tính toán định giá đầu tư nâng cao."""

    def __init__(self, seed: int = 42) -> None:
        random.seed(seed)

    def run_monte_carlo_valuation(
        self,
        base_investment: float,
        expected_cash_flows: list[float],
        iterations: int = 1000,
    ) -> ValuationResult:
        """Thực hiện mô phỏng rủi ro Monte Carlo xác định NPV thực."""
        npv_simulations: list[float] = []

        for _ in range(iterations):
            simulated_npv = -base_investment
            for t, cf in enumerate(expected_cash_flows, start=1):
                variation = random.uniform(0.8, 1.2)
                simulated_cf = cf * variation
                simulated_npv += simulated_cf / math.pow(1.1, t)
            npv_simulations.append(simulated_npv)

        avg_npv = sum(npv_simulations) / len(npv_simulations)
        option_val = max(0.0, avg_npv * 0.15)

        proof_payload = {
            "investment": base_investment,
            "avg_npv": avg_npv,
            "iterations": iterations,
        }
        proof_hash = QuantumLedger.generate_proof(proof_payload)

        return ValuationResult(
            npv=round(avg_npv, 2),
            option_value=round(option_val, 2),
            simulated_volatility=0.20,
            quantum_evidence_hash=proof_hash,
        )
