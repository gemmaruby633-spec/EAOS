"""Value Streams Mapping and Execution Engine (BIZBOK Standard)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ValueStageDTO(BaseModel):
    """Value Stage in an Enterprise Value Stream."""

    model_config = ConfigDict(frozen=True)

    stage_id: str = Field(..., description="Stage ID e.g. vs-lead")
    name: str = Field(..., description="Stage name")
    value_created: str = Field(default="")


class ValueStreamDTO(BaseModel):
    """Value Stream mapping end-to-end business value creation."""

    model_config = ConfigDict(frozen=True)

    stream_id: str = Field(..., description="Stream ID e.g. vs-lead-to-cash")
    name: str = Field(..., description="Value stream name")
    stages: list[ValueStageDTO] = Field(default_factory=list)


class ValueStreamEngine:
    """Engine managing enterprise value stream mappings."""

    def get_lead_to_cash_stream(self) -> ValueStreamDTO:
        """Return standard Lead-to-Cash Value Stream."""
        return ValueStreamDTO(
            stream_id="vs-lead-to-cash",
            name="Lead-to-Cash Value Stream",
            stages=[
                ValueStageDTO(
                    stage_id="stg-01",
                    name="Lead Generation",
                    value_created="Qualified Prospect",
                ),
                ValueStageDTO(
                    stage_id="stg-02",
                    name="Order Execution",
                    value_created="Fulfilled Customer Order",
                ),
            ],
        )
