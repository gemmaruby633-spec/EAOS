"""Tự dọn dẹp thư mục rác và phục hồi vẹn toàn package RUNTIME."""

from __future__ import annotations

import shutil
from pathlib import Path


class SelfHealingArchiver:
    """Dọn dẹp thư mục rác IDE và tệp tạm dư thừa."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def purge_junk_folders_and_pycache(self) -> int:
        """Xóa sạch các thư mục rác claude, cline, gitkraken và __pycache__."""
        purged = 0
        junk_names = ["claude", "cline", "gitkraken", "__pycache__"]
        for jname in junk_names:
            for item in self.root_dir.glob(f"**/{jname}"):
                if item.is_dir():
                    shutil.rmtree(item)
                    purged += 1
        return purged
