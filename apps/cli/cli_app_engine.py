"""Động cơ ứng dụng CLI Console."""

from __future__ import annotations


class CliAppEngine:
    """Khởi chạy CLI Console."""

    def execute_command(self, cmd: str) -> str:
        """Thực thi lệnh CLI."""
        return f"EXECUTED_{cmd}"
