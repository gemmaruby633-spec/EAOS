"""Sổ cái bằng chứng xuất xứ sản phẩm chống lượng tử."""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any


class QuantumProductLedger:
    """Đúc bằng chứng mã hóa SHA3-256 cho nguồn gốc sản phẩm."""

    @staticmethod
    def generate_product_proof(
        product_id: str,
        payload: dict[str, Any],
        secret_key: str = "EAOS_PROD_PQ_2026",
    ) -> str:
        """Sinh mã băm nguồn gốc bằng chứng chống lượng tử."""
        serialized = json.dumps(payload, sort_keys=True)
        timestamp = str(time.time_ns())
        raw_data = f"{product_id}:{serialized}:{timestamp}:{secret_key}".encode()
        hasher = hashlib.sha3_256()
        hasher.update(raw_data)
        return f"pq_product_{hasher.hexdigest()}"
