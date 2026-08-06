"""Tự phục hồi và dọn dẹp thư mục quy tắc."""

from __future__ import annotations

import shutil
from pathlib import Path


class SelfHealingArchiver:
    """Quản lý tự dọn dẹp pycache và bổ sung __init__.py."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def purge_pycache(self) -> int:
        """Xóa toàn bộ thư mục rác __pycache__."""
        purged = 0
        for pycache in self.root_dir.glob("**/__pycache__"):
            if pycache.is_dir():
                shutil.rmtree(pycache)
                purged += 1
        return purged
