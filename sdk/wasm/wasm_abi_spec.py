"""Đặc tả ABI WebAssembly."""

from __future__ import annotations


class WasmAbiSpec:
    """Đặc tả bộ nhớ WASM."""

    @staticmethod
    def get_abi_version() -> str:
        """Lấy phiên bản WASM ABI."""
        return "v1.0.0-wasm"
