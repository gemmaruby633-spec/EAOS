"""Application use cases for Universal EA Frameworks Ingestion."""

import uuid

from packages.frameworks.domain.models import (
    EAFrameworkType,
    FrameworkProfile,
    MetamodelMapping,
)


class IngestFrameworkMetamodelUseCase:
    """Use case ingesting and mapping an EA Framework into EAOS."""

    def execute(
        self,
        framework_type: EAFrameworkType,
        mappings: list[MetamodelMapping],
    ) -> FrameworkProfile:
        """Ingests framework schema into universal registry."""
        p_id = f"FWK-{uuid.uuid4().hex[:8].upper()}"
        return FrameworkProfile(
            profile_id=p_id,
            framework_type=framework_type,
            name=f"Ingested Metamodel for {framework_type.value}",
            mappings=tuple(mappings),
            is_active=True,
        )
