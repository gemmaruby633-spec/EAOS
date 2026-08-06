"""Sổ cái vết chứng nhận an ninh chống lượng tử."""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any


class QuantumSecurityLedger:
    """Đúc bằng chứng mã hóa an ninh."""

    @staticmethod
    def generate_security_proof(
        subject_id: str,
        payload: dict[str, Any],
        secret_key: str = "EAOS_SEC_PQ_2026",
    ) -> str:
        """Sinh mã băm bằng chứng an ninh không thể sửa đổi."""
        serialized = json.dumps(payload, sort_keys=True)
        timestamp = str(time.time_ns())
        raw_bytes = f"{subject_id}:{serialized}:{timestamp}:{secret_key}".encode()
        hasher = hashlib.sha3_256()
        hasher.update(raw_bytes)
        return f"pq_sec_{hasher.hexdigest()}"
