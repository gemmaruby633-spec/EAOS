"""Application use cases for IT Management & Governance Ingestion."""

import uuid

from packages.it_governance.domain.models import (
    ITControlObjective,
    ITGovernanceFrameworkType,
    ITGovernanceProfile,
)


class IngestITGovernanceFrameworkUseCase:
    """Use case ingesting IT Management frameworks into EAOS."""

    def execute(
        self,
        framework_type: ITGovernanceFrameworkType,
        controls: list[ITControlObjective],
    ) -> ITGovernanceProfile:
        """Ingests IT governance controls into central registry."""
        p_id = f"ITGOV-{uuid.uuid4().hex[:8].upper()}"
        return ITGovernanceProfile(
            profile_id=p_id,
            framework_type=framework_type,
            name=f"Ingested IT Profile for {framework_type.value}",
            controls=tuple(controls),
        )
