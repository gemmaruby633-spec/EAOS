"""Application use cases for Integration Architecture Ingestion."""

import uuid

from packages.integration_architecture.domain.models import (
    IntegrationContractPattern,
    IntegrationFrameworkProfile,
    IntegrationFrameworkType,
)


class IngestIntegrationFrameworkUseCase:
    """Use case ingesting Integration Architecture frameworks into EAOS."""

    def execute(
        self,
        framework_type: IntegrationFrameworkType,
        patterns: list[IntegrationContractPattern],
    ) -> IntegrationFrameworkProfile:
        """Ingests integration patterns into central registry."""
        p_id = f"INTFWK-{uuid.uuid4().hex[:8].upper()}"
        return IntegrationFrameworkProfile(
            profile_id=p_id,
            framework_type=framework_type,
            name=f"Ingested Integration Profile for {framework_type.value}",
            patterns=tuple(patterns),
        )
