"""Application use cases for Business Architecture Ingestion."""

import uuid

from packages.business_architecture.domain.models import (
    BusinessElementMapping,
    BusinessFrameworkProfile,
    BusinessFrameworkType,
)


class IngestBusinessFrameworkUseCase:
    """Use case ingesting Business Architecture frameworks into EAOS."""

    def execute(
        self,
        framework_type: BusinessFrameworkType,
        mappings: list[BusinessElementMapping],
    ) -> BusinessFrameworkProfile:
        """Ingests business framework schema into registry."""
        p_id = f"BIZFWK-{uuid.uuid4().hex[:8].upper()}"
        return BusinessFrameworkProfile(
            profile_id=p_id,
            framework_type=framework_type,
            name=f"Ingested Business Model for {framework_type.value}",
            mappings=tuple(mappings),
        )
