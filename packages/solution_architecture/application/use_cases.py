"""Application use cases for Solution Architecture Ingestion."""

import uuid

from packages.solution_architecture.domain.models import (
    PatternComplianceRule,
    SolutionArchitectureProfile,
    SolutionPatternType,
)


class IngestSolutionPatternUseCase:
    """Use case ingesting Solution Architecture patterns into EAOS."""

    def execute(
        self,
        pattern_type: SolutionPatternType,
        rules: list[PatternComplianceRule],
    ) -> SolutionArchitectureProfile:
        """Ingests solution pattern rules into central registry."""
        p_id = f"SOLFWK-{uuid.uuid4().hex[:8].upper()}"
        return SolutionArchitectureProfile(
            profile_id=p_id,
            pattern_type=pattern_type,
            name=f"Ingested Pattern for {pattern_type.value}",
            rules=tuple(rules),
        )
