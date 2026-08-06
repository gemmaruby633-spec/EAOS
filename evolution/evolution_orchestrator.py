"""Master Self-Evolution Engine Orchestrator."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from evolution.fitness.fitness_evaluator import (
    ArchitectureFitnessEvaluator,
    FitnessEvaluationDTO,
)
from evolution.lineage.lineage_tracker import ArchitecturalLineageTracker
from evolution.migrations.migration_engine import (
    ArchitecturalMigrationEngine,
)
from evolution.roadmaps.roadmap_planner import StrategicRoadmapPlanner


class EvolutionSummaryDTO(BaseModel):
    """Summary DTO for enterprise self-evolution status."""

    model_config = ConfigDict(frozen=True)

    maturity_level: str = Field(default="Level 5 - Evolutionary")
    fitness_summary: FitnessEvaluationDTO
    active_horizons_count: int = Field(default=6)
    evolution_loop_active: bool = Field(default=True)


class EAOSEvolutionOrchestrator:
    """Master Orchestrator binding Fitness, Lineage, Migrations & Roadmaps."""

    def __init__(self) -> None:
        self.evaluator = ArchitectureFitnessEvaluator()
        self.tracker = ArchitecturalLineageTracker()
        self.migration = ArchitecturalMigrationEngine()
        self.roadmap = StrategicRoadmapPlanner()

    def get_evolution_status(self) -> EvolutionSummaryDTO:
        """Generate status summary for self-evolving architecture."""
        fit = self.evaluator.evaluate_fitness(violations_count=0, total_rules=20)
        horizons = self.roadmap.get_active_horizons()

        return EvolutionSummaryDTO(
            maturity_level="Level 5 - Evolutionary",
            fitness_summary=fit,
            active_horizons_count=len(horizons),
            evolution_loop_active=True,
        )
