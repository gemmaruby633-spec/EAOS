"""Tự dọn dẹp thư mục rác __pycache__ và phục hồi tệp thiếu."""

from __future__ import annotations

import shutil
from pathlib import Path


class SelfHealingArchiver:
    """Dọn rác __pycache__ và phục hồi vẹn toàn package SRC."""

    def __init__(self) -> None:
        self.root_dir = Path(__file__).parent.parent

    def purge_pycache(self) -> int:
        """Xóa toàn bộ thư mục rác __pycache__."""
        purged = 0
        for item in self.root_dir.glob("**/__pycache__"):
            if item.is_dir():
                shutil.rmtree(item)
                purged += 1
        return purged
