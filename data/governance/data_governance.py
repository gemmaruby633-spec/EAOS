"""Data Governance and PII Classification Engine (DAMA-DMBOK2)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DataClassificationDTO(BaseModel):
    """Value object representing data security classification."""

    model_config = ConfigDict(frozen=True)

    field_name: str = Field(..., description="Field name e.g. email")
    classification: str = Field(default="PII")
    is_encrypted: bool = Field(default=True)


class DataGovernanceEngine:
    """Engine enforcing data classification and PII redaction."""

    def redact_pii_data(self, data: dict[str, str]) -> dict[str, str]:
        """Redact sensitive PII fields in data dictionary."""
        redacted = dict(data)
        pii_keys = {"email", "phone", "ssn", "password"}
        for k in redacted:
            if k.lower() in pii_keys:
                redacted[k] = "[REDACTED_PII]"
        return redacted
