"""Enterprise Taxonomy and Domain Hierarchy Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TaxonomyNodeDTO(BaseModel):
    """Value object representing a taxonomy hierarchy node."""

    model_config = ConfigDict(frozen=True)

    node_id: str = Field(..., description="Node ID e.g. tax-sales")
    label: str = Field(..., description="Display label")
    parent_id: str | None = Field(default=None)


class EnterpriseTaxonomyEngine:
    """Engine managing domain classification taxonomies."""

    def get_domain_taxonomies(self) -> list[TaxonomyNodeDTO]:
        """Return baseline enterprise taxonomy tree."""
        return [
            TaxonomyNodeDTO(node_id="tax-core", label="Enterprise Core"),
            TaxonomyNodeDTO(
                node_id="tax-governance",
                label="Governance & Compliance",
                parent_id="tax-core",
            ),
        ]
