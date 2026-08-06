"""Unit test suite for EAOS platform services."""

from platforms.cache.redis_rate_limiter import RedisDistributedRateLimiter
from platforms.database.circuit_breaker_pool import DatabaseCircuitBreakerPool


def test_distributed_cache_adapter() -> None:
    limiter = RedisDistributedRateLimiter()
    res = limiter.check_rate_limit("127.0.0.1")
    assert res.allowed is True


def test_circuit_breaker_pool() -> None:
    pool = DatabaseCircuitBreakerPool()
    health = pool.get_pool_health()
    assert health.is_healthy is True
