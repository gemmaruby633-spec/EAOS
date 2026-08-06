"""Động cơ điều tuyến Service Mesh."""

from __future__ import annotations


class ServiceMeshRouter:
    """Quản lý điều tuyến Sidecar Proxy."""

    def route(self, source: str, target: str) -> bool:
        """Điều hướng cuộc gọi vi dịch vụ."""
        return len(source) > 0 and len(target) > 0
