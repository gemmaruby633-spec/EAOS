"""Security and Business Data Classification Engine."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ClassificationLevel(StrEnum):
    """Data security classification levels."""

    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"


class ClassificationPolicyDTO(BaseModel):
    """Value object representing a data classification policy."""

    model_config = ConfigDict(frozen=True)

    field_name: str
    level: ClassificationLevel = Field(default=ClassificationLevel.INTERNAL)


class DataClassificationEngine:
    """Engine assessing data sensitivity classification."""

    def classify_field(self, field_name: str) -> ClassificationPolicyDTO:
        """Determine classification level for field."""
        if field_name.lower() in {"ssn", "password", "secret_key"}:
            return ClassificationPolicyDTO(
                field_name=field_name,
                level=ClassificationLevel.CONFIDENTIAL,
            )
        return ClassificationPolicyDTO(field_name=field_name, level=ClassificationLevel.INTERNAL)
