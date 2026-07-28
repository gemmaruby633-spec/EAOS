"""Application use cases for Data Architecture Ingestion."""

import uuid

from packages.data_architecture.domain.models import (
    DataFrameworkProfile,
    DataFrameworkType,
    DataGovernanceRule,
)


class IngestDataFrameworkUseCase:
    """Use case ingesting Data Architecture frameworks into EAOS."""

    def execute(
        self,
        framework_type: DataFrameworkType,
        rules: list[DataGovernanceRule],
    ) -> DataFrameworkProfile:
        """Ingests data framework governance rules into central registry."""
        p_id = f"DATAFWK-{uuid.uuid4().hex[:8].upper()}"
        return DataFrameworkProfile(
            profile_id=p_id,
            framework_type=framework_type,
            name=f"Ingested Data Profile for {framework_type.value}",
            rules=tuple(rules),
        )
