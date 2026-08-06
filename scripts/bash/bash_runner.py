"""Động cơ điều phối Bash Scripts."""

from __future__ import annotations


class BashRunner:
    """Điều phối kịch bản Bash/POSIX."""

    def run_sh_script(self, script_path: str) -> bool:
        """Chạy kịch bản Shell."""
        return script_path.endswith(".sh")
