"""Patch Engine Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.solution_architecture.domain.patch_models import (
    PatchResult,
)


@runtime_checkable
class PatchEnginePort(Protocol):
    """Port protocol for safe file patching and backups."""

    async def apply_patch(self, target_file: str, new_content: str) -> PatchResult: ...

    async def restore_backup(self, backup_path: str) -> bool: ...
