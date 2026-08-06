"""Cryptographic Utilities and Hash Evidence Helpers."""

from __future__ import annotations

import hashlib


class CryptographicUtils:
    """Helper class providing SHA-256 evidence hashing."""

    @staticmethod
    def calculate_sha256(payload: str) -> str:
        """Calculate SHA-256 hash string for payload."""
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
