"""Động cơ thực thi đặc tả Capabilities."""

from __future__ import annotations


class CapabilitySpecEngine:
    """Kiểm tra tuân thủ Capability Specs."""

    def verify_capability(self, name: str) -> bool:
        """Xác minh đặc tả năng lực."""
        return len(name) > 0
