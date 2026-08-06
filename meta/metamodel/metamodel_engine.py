"""Universal Enterprise Metamodel Engine (Sprint 3.1)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MetaAttributeDTO(BaseModel):
    """Value object representing an attribute in Meta-Model."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Attribute name")
    data_type: str = Field(default="string")
    is_required: bool = Field(default=True)


class MetaEntityDTO(BaseModel):
    """Value object representing an Entity in Meta-Model."""

    model_config = ConfigDict(frozen=True)

    entity_id: str = Field(..., description="Entity ID e.g. meta-customer")
    name: str = Field(..., description="Entity name")
    attributes: list[MetaAttributeDTO] = Field(default_factory=list)


class UniversalMetamodelEngine:
    """Engine managing meta-level schema definitions."""

    def get_meta_entities(self) -> list[MetaEntityDTO]:
        """Return standard meta-model entity definitions."""
        return [
            MetaEntityDTO(
                entity_id="meta-capability",
                name="Capability",
                attributes=[
                    MetaAttributeDTO(name="id", data_type="string"),
                    MetaAttributeDTO(name="owner", data_type="string"),
                ],
            )
        ]
