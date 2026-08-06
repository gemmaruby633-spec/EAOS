"""Master Digital Twin Orchestrator Engine."""

from __future__ import annotations

from digitaltwin.models.twin_models import (
    ComponentTwinStateDTO,
    EnterpriseTwinStateDTO,
)
from digitaltwin.replay.twin_replay import TwinEventReplayEngine
from digitaltwin.simulation.twin_simulation import (
    EnterpriseTwinSimulationEngine,
    TwinSimulationResultDTO,
)


class EnterpriseDigitalTwinOrchestrator:
    """Master Orchestrator coordinating Twin State, Simulation & Replay."""

    def __init__(self) -> None:
        self.simulator = EnterpriseTwinSimulationEngine()
        self.replay = TwinEventReplayEngine()

    def get_current_twin_state(self) -> EnterpriseTwinStateDTO:
        """Construct current Digital Twin state snapshot."""
        comps = [
            ComponentTwinStateDTO(
                component_id="api_gateway",
                component_name="FastAPI Gateway",
                health_score=100.0,
            ),
            ComponentTwinStateDTO(
                component_id="postgres_lake",
                component_name="PostgreSQL pgvector",
                health_score=100.0,
            ),
            ComponentTwinStateDTO(
                component_id="neo4j_graph",
                component_name="Neo4j Knowledge Graph",
                health_score=100.0,
            ),
        ]
        return EnterpriseTwinStateDTO(
            twin_id="dtwin-001",
            overall_health_score=100.0,
            active_components_count=len(comps),
            components=comps,
        )

    def simulate_change(self, scenario_name: str) -> TwinSimulationResultDTO:
        """Run what-if simulation scenario on digital twin."""
        state = self.get_current_twin_state()
        return self.simulator.run_what_if_simulation(state, scenario_name)
