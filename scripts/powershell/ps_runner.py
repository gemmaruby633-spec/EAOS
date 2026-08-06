"""Động cơ điều phối PowerShell Scripts."""

from __future__ import annotations


class PsRunner:
    """Điều phối kịch bản PowerShell."""

    def run_ps_script(self, script_path: str) -> bool:
        """Chạy kịch bản PowerShell."""
        return script_path.endswith(".ps1")
