"""EAOS Platform Client SDK for external applications and AI Agents."""

import httpx
from pydantic import BaseModel, ConfigDict


class PlatformStatusDTO(BaseModel):
    """Value object representing EAOS platform status response."""

    model_config = ConfigDict(frozen=True)

    system: str
    status: str
    version: str
    governance: str


class EAOSPlatformClient:
    """Client SDK interacting with EAOS Enterprise Platform."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
        timeout_sec: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_sec = timeout_sec

    def get_platform_status(self) -> PlatformStatusDTO:
        """Fetches live status probe from EAOS Platform."""
        with httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout_sec,
        ) as client:
            resp = client.get("/")
            resp.raise_for_status()
            data = resp.json()
            return PlatformStatusDTO(
                system=str(data.get("system", "EAOS")),
                status=str(data.get("status", "ACTIVE")),
                version=str(data.get("version", "0.1.0")),
                governance=str(data.get("governance", "v3.0")),
            )


if __name__ == "__main__":
    sdk = EAOSPlatformClient()
    print("✔ EAOS Platform SDK initialized successfully!")
