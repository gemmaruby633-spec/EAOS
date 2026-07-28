"""Pydantic Settings and Environment Configuration for Gateway."""

from pydantic import BaseModel


class GatewaySettings(BaseModel):
    """Application level environment settings."""

    app_name: str = "EAOS API Gateway"
    version: str = "0.1.0"
    environment: str = "production"
    database_url: str = "postgresql://eaos:eaos@localhost:5433/eaos"


settings = GatewaySettings()
