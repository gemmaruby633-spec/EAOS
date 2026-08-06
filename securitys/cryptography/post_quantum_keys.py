"""Post quantum key manager."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KeyFingerprintDTO:
    """Key fingerprint DTO."""

    public_key_fingerprint: str = "dilithium3_fingerprint_001"
    key_length_bits: int = 2560


class PostQuantumKeyManager:
    """Post quantum key manager."""

    def generate_key_fingerprint(self, key_id: str = "key_001") -> KeyFingerprintDTO:
        """Generate key fingerprint."""
        return KeyFingerprintDTO()
