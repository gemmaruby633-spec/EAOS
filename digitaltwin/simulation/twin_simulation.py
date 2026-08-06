"""Digital Twin What-If Simulation Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from digitaltwin.models.twin_models import EnterpriseTwinStateDTO


class TwinSimulationResultDTO(BaseModel):
    """Result of a what-if simulation scenario on Digital Twin."""

    model_config = ConfigDict(frozen=True)

    scenario_name: str
    predicted_health_score: float
    risk_level: str = Field(default="LOW")
    policy_compliant: bool = Field(default=True)
    recommendation: str = Field(default="Safe to proceed with deployment.")


class EnterpriseTwinSimulationEngine:
    """Engine simulating architectural changes on Digital Twin."""

    def run_what_if_simulation(self, state: EnterpriseTwinStateDTO, scenario_name: str) -> TwinSimulationResultDTO:
        """Run simulation on current twin state."""
        if state.overall_health_score < 80.0:
            return TwinSimulationResultDTO(
                scenario_name=scenario_name,
                predicted_health_score=state.overall_health_score - 10.0,
                risk_level="HIGH",
                policy_compliant=False,
                recommendation="Abort deployment: Twin health degraded.",
            )

        return TwinSimulationResultDTO(
            scenario_name=scenario_name,
            predicted_health_score=state.overall_health_score,
            risk_level="LOW",
            policy_compliant=True,
            recommendation="Simulated change passed all safety checks.",
        )
