"""Unified Patch Engine Adapter with Backup Protection."""

from __future__ import annotations

import difflib
from datetime import UTC, datetime
from pathlib import Path

from packages.solution_architecture.domain.patch_models import (
    BackupRecord,
    PatchResult,
)
from packages.solution_architecture.ports.patch_port import (
    PatchEnginePort,
)


class UnifiedPatchAdapter(PatchEnginePort):
    """Adapter performing atomic file backup and patch application."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()
        self.backup_dir = self.root / ".eaos_backups"

    async def apply_patch(self, target_file: str, new_content: str) -> PatchResult:
        target_path = (self.root / target_file).resolve()
        try:
            target_path.relative_to(self.root)
        except ValueError:
            return PatchResult(
                success=False,
                target_file=target_file,
                error_message="Path traversal violation detected.",
            )

        old_content = ""
        backup_rec: BackupRecord | None = None

        if target_path.exists():
            old_content = target_path.read_text(encoding="utf-8")
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            ts_str = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            b_name = f"{target_path.stem}_{ts_str}{target_path.suffix}.bak"
            b_path = self.backup_dir / b_name
            b_path.write_text(old_content, encoding="utf-8")
            backup_rec = BackupRecord(
                original_path=str(target_path),
                backup_path=str(b_path),
            )

        diff_lines = list(
            difflib.unified_diff(
                old_content.splitlines(keepends=True),
                new_content.splitlines(keepends=True),
                fromfile=f"a/{target_file}",
                tofile=f"b/{target_file}",
            )
        )
        diff_str = "".join(diff_lines)

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(new_content, encoding="utf-8")

        return PatchResult(
            success=True,
            target_file=target_file,
            diff_summary=diff_str or "No lines changed.",
            backup=backup_rec,
        )

    async def restore_backup(self, backup_path: str) -> bool:
        b_file = Path(backup_path)
        if not b_file.exists():
            return False
        content = b_file.read_text(encoding="utf-8")
        orig_name = b_file.name.split("_")[0]
        orig_file = self.root / orig_name
        orig_file.write_text(content, encoding="utf-8")
        return True
