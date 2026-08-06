"""Sổ cái vết chứng nhận chính sách chống lượng tử."""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any


class QuantumSrcLedger:
    """Đúc bằng chứng mã hóa chính sách domain."""

    @staticmethod
    def generate_src_proof(
        policy_id: str,
        payload: dict[str, Any],
        secret_key: str = "EAOS_SRC_PQ_2026",
    ) -> str:
        """Sinh mã băm chứng nhận không thể sửa đổi."""
        serialized = json.dumps(payload, sort_keys=True)
        timestamp = str(time.time_ns())
        raw_bytes = f"{policy_id}:{serialized}:{timestamp}:{secret_key}".encode()
        hasher = hashlib.sha3_256()
        hasher.update(raw_bytes)
        return f"pq_src_{hasher.hexdigest()}"
