"""Mô hình DTO cho hệ thống Vi dịch vụ Doanh nghiệp (SERVICES)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ServiceState(StrEnum):
    """Trạng thái dịch vụ."""

    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    DEGRADED = "DEGRADED"


@dataclass(frozen=True)
class ServiceDescriptor:
    """Đặc tả Dịch vụ."""

    service_id: str
    name: str
    port: int
    health_endpoint: str = "/health"


@dataclass
class ServiceCallResult:
    """Kết quả gọi vi dịch vụ."""

    service_id: str
    status_code: int
    payload: dict[str, str] = field(default_factory=dict)
    quantum_hash: str = ""
