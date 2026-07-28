"""Application use cases for Security Architecture Ingestion."""

import uuid

from packages.security_architecture.domain.models import (
    SecurityControlPolicy,
    SecurityFrameworkProfile,
    SecurityFrameworkType,
)


class IngestSecurityFrameworkUseCase:
    """Use case ingesting Security Architecture frameworks into EAOS."""

    def execute(
        self,
        framework_type: SecurityFrameworkType,
        controls: list[SecurityControlPolicy],
    ) -> SecurityFrameworkProfile:
        """Ingests security framework controls into central registry."""
        p_id = f"SECFWK-{uuid.uuid4().hex[:8].upper()}"
        return SecurityFrameworkProfile(
            profile_id=p_id,
            framework_type=framework_type,
            name=f"Ingested Security Profile for {framework_type.value}",
            controls=tuple(controls),
        )
