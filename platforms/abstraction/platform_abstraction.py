"""Platform Abstraction Layer for Enterprise Hardware and Cloud."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PlatformAbstractionDTO(BaseModel):
    """Value object representing platform hardware abstraction."""

    model_config = ConfigDict(frozen=True)

    platform_type: str = Field(default="HYBRID_CLOUD")
    cpu_cores: int = Field(default=8)
    is_airgapped: bool = Field(default=False)


class PlatformAbstractionEngine:
    """Engine providing unified abstraction for OS and Cloud Hardware."""

    def get_platform_info(self) -> PlatformAbstractionDTO:
        """Return platform hardware abstraction DTO."""
        return PlatformAbstractionDTO(
            platform_type="HYBRID_CLOUD",
            cpu_cores=8,
            is_airgapped=False,
        )
