"""Mô hình DTO cho Trạng thái Vận hành Runtime (RUNTIME)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ServiceHealth(StrEnum):
    """Trạng thái sức khỏe dịch vụ."""

    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"


@dataclass(frozen=True)
class ServiceInstance:
    """Thông tin đăng ký dịch vụ."""

    service_id: str
    name: str
    endpoint: str
    status: ServiceHealth = ServiceHealth.HEALTHY


@dataclass
class RuntimeStateSnapshot:
    """Ảnh chụp trạng thái vận hành hệ thống."""

    active_sessions: int
    active_services: int
    cache_hit_ratio: float
    quantum_proof_hash: str
