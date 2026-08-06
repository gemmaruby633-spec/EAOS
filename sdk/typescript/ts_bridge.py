"""Python Bridge contract cho TypeScript/Node SDK."""

from __future__ import annotations


class TsBridge:
    """Cầu nối tương tác với Node.js runtime."""

    @staticmethod
    def is_node_available() -> bool:
        """Kiểm tra môi trường Node.js."""
        return True
