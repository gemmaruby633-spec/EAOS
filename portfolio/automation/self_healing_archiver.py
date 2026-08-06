"""Công cụ Tự Phục Hồi, Sao Lưu và Dọn Rác Thư Mục."""

from __future__ import annotations

import shutil
from pathlib import Path


class SelfHealingArchiver:
    """Quản lý tự phục hồi cấu trúc thư mục và sao lưu định kỳ."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def purge_pycache(self) -> int:
        """Xóa sạch toàn bộ thư mục rác __pycache__."""
        purged_count = 0
        for pycache in self.root_dir.glob("**/__pycache__"):
            if pycache.is_dir():
                shutil.rmtree(pycache)
                purged_count += 1
        return purged_count

    def verify_and_repair_package_integrity(self, expected_subdirs: list[str]) -> list[str]:
        """Kiểm tra và tự bổ sung __init__.py cho các thư mục con bị thiếu."""
        repaired: list[str] = []
        for subdir in expected_subdirs:
            target = self.root_dir / subdir
            target.mkdir(parents=True, exist_ok=True)
            init_file = target / "__init__.py"
            if not init_file.exists():
                init_file.write_text(f'"""Auto-generated init for {subdir}."""\n')
                repaired.append(subdir)
        return repaired
