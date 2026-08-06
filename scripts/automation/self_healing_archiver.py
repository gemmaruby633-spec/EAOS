"""Tự phục hồi và dọn dẹp phân hệ SCRIPTS."""

from __future__ import annotations

import shutil
from pathlib import Path


class SelfHealingArchiver:
    """Dọn rác __pycache__ và phục hồi tệp thiếu."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def purge_pycache(self) -> int:
        """Xóa toàn bộ __pycache__ trong package."""
        purged = 0
        for item in self.root_dir.glob("**/__pycache__"):
            if item.is_dir():
                shutil.rmtree(item)
                purged += 1
        return purged
