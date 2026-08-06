"""Động cơ xử lý Compiler Spec Schema."""

from __future__ import annotations


class CompilerSchemaEngine:
    """Quản lý đặc tả biên dịch IR."""

    def verify_spec(self, spec_id: str) -> bool:
        """Xác minh chuẩn biên dịch."""
        return spec_id.startswith("SPEC-")
