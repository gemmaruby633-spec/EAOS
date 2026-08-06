"""Python Bridge CGo contract cho Go SDK."""

from __future__ import annotations


class GoBridge:
    """Cầu nối tương tác với Go C-Shared Library."""

    @staticmethod
    def is_go_available() -> bool:
        """Kiểm tra khả năng tích hợp Go FFI."""
        return True
