"""Application use cases for Process Architecture Ingestion."""

import uuid

from packages.process_architecture.domain.models import (
    ProcessFrameworkProfile,
    ProcessFrameworkType,
    ProcessMappingElement,
)


class IngestProcessFrameworkUseCase:
    """Use case ingesting Process Architecture frameworks into EAOS."""

    def execute(
        self,
        framework_type: ProcessFrameworkType,
        mappings: list[ProcessMappingElement],
    ) -> ProcessFrameworkProfile:
        """Ingests process framework schema into registry."""
        p_id = f"PROCFWK-{uuid.uuid4().hex[:8].upper()}"
        return ProcessFrameworkProfile(
            profile_id=p_id,
            framework_type=framework_type,
            name=f"Ingested Process Model for {framework_type.value}",
            mappings=tuple(mappings),
        )
