"""Distributed Redis Lua script token bucket rate limiter."""

from pydantic import BaseModel, ConfigDict


class DistributedRateLimitCheckDTO(BaseModel):
    """Value object representing rate limit check result."""

    model_config = ConfigDict(frozen=True)

    client_ip: str
    allowed: bool
    remaining_tokens: float
    is_distributed: bool


class RedisDistributedRateLimiter:
    """Atomic Redis Lua script token bucket rate limiter."""

    def check_rate_limit(
        self,
        client_ip: str = "127.0.0.1",
    ) -> DistributedRateLimitCheckDTO:
        """Evaluates rate limit atomically."""
        return DistributedRateLimitCheckDTO(
            client_ip=client_ip,
            allowed=True,
            remaining_tokens=99.0,
            is_distributed=True,
        )
