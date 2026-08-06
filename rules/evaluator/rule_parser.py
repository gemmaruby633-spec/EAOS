"""Động cơ đọc và phân tích cấu trúc quy tắc YAML."""

from __future__ import annotations

from typing import Any


class RuleParser:
    """Phân tích nội dung tệp YAML quy tắc."""

    @staticmethod
    def parse_yaml_metadata(yaml_content: str) -> dict[str, Any]:
        """Trích xuất thuộc tính cơ bản của quy tắc."""
        lines = yaml_content.strip().splitlines()
        parsed: dict[str, Any] = {}
        for line in lines:
            if ":" in line and not line.startswith("#"):
                k, v = line.split(":", 1)
                parsed[k.strip()] = v.strip().strip('"')
        return parsed
