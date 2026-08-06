"""Master Enterprise Meta-System Orchestrator Engine."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from meta.classification.classification_engine import (
    DataClassificationEngine,
)
from meta.metamodel.metamodel_engine import UniversalMetamodelEngine
from meta.taxonomy.taxonomy_engine import EnterpriseTaxonomyEngine


class MetaSystemSummaryDTO(BaseModel):
    """Summary DTO for enterprise meta-system status."""

    model_config = ConfigDict(frozen=True)

    meta_entities_count: int = Field(default=1)
    taxonomies_count: int = Field(default=2)
    classification_active: bool = Field(default=True)


class EAOSEnterpriseMetaSystem:
    """Master Orchestrator for Metamodels, Taxonomies, & Classification."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.metamodel = UniversalMetamodelEngine()
        self.taxonomy = EnterpriseTaxonomyEngine()
        self.classification = DataClassificationEngine()

    def get_meta_system_summary(self) -> MetaSystemSummaryDTO:
        """Generate summary of enterprise meta-system status."""
        entities = self.metamodel.get_meta_entities()
        taxs = self.taxonomy.get_domain_taxonomies()

        return MetaSystemSummaryDTO(
            meta_entities_count=len(entities),
            taxonomies_count=len(taxs),
            classification_active=True,
        )
