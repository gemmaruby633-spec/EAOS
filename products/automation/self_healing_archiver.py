"""Động cơ tự phục hồi và dọn rác phân hệ PRODUCTS."""

from __future__ import annotations

import shutil
from pathlib import Path


class SelfHealingArchiver:
    """Xóa pycache và bổ sung __init__.py tự động."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def purge_pycache(self) -> int:
        """Xóa toàn bộ __pycache__ trong phân hệ."""
        purged = 0
        for pycache in self.root_dir.glob("**/__pycache__"):
            if pycache.is_dir():
                shutil.rmtree(pycache)
                purged += 1
        return purged

    def repair_missing_inits(self, required_dirs: list[str]) -> list[str]:
        """Đảm bảo mọi thư mục con đều có __init__.py."""
        repaired: list[str] = []
        for rd in required_dirs:
            target = self.root_dir / rd
            target.mkdir(parents=True, exist_ok=True)
            init_file = target / "__init__.py"
            if not init_file.exists():
                init_file.write_text(f'"""Init for {rd}."""\n')
                repaired.append(rd)
            return repaired
        return None
