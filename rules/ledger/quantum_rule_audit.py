"""Sổ cái bằng chứng thực thi quy tắc chống lượng tử."""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any


class QuantumRuleAudit:
    """Tạo mã băm SHA3-256 xác thực lịch sử kiểm toán quy tắc."""

    @staticmethod
    def generate_audit_proof(
        rule_id: str,
        payload: dict[str, Any],
        secret_key: str = "EAOS_RULES_PQ_2026",
    ) -> str:
        """Đúc bằng chứng mã hóa không thể sửa đổi."""
        serialized = json.dumps(payload, sort_keys=True)
        timestamp = str(time.time_ns())
        raw_bytes = f"{rule_id}:{serialized}:{timestamp}:{secret_key}".encode()
        hasher = hashlib.sha3_256()
        hasher.update(raw_bytes)
        return f"pq_rule_{hasher.hexdigest()}"
