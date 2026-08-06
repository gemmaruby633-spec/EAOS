"""Mô hình DTO cho hệ thống Polyglot SDK (SDK)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class SdkLanguage(StrEnum):
    """Ngôn ngữ hỗ trợ SDK."""

    PYTHON = "PYTHON"
    GO = "GO"
    TYPESCRIPT = "TYPESCRIPT"
    WASM = "WASM"


@dataclass(frozen=True)
class SdkConfig:
    """Cấu hình kết nối SDK."""

    endpoint: str = "http://127.0.0.1:8000"
    timeout_seconds: float = 30.0
    enable_quantum_proof: bool = True


@dataclass
class SdkCallResponse:
    """Kết quả phản hồi cuộc gọi API qua SDK."""

    success: bool
    data: dict[str, str] = field(default_factory=dict)
    proof_hash: str = ""
