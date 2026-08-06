"""Mô hình DTO cho hệ thống Scripts Vận hành (SCRIPTS)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ScriptCategory(StrEnum):
    """Phân loại Script."""

    POWERSHELL = "POWERSHELL"
    BASH = "BASH"
    PYTHON = "PYTHON"
    CICD = "CICD"
    HEALING = "HEALING"


@dataclass(frozen=True)
class ScriptDefinition:
    """Định nghĩa script vận hành."""

    script_id: str
    name: str
    category: ScriptCategory
    file_path: str


@dataclass
class ScriptExecutionResult:
    """Kết quả thực thi script."""

    script_id: str
    exit_code: int
    output: str
    proof_hash: str = ""
