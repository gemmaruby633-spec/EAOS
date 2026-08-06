"""Enterprise Schema Validation Helpers."""

from __future__ import annotations

from typing import Any


class SchemaValidatorHelper:
    """Helper class validating input dictionaries against required keys."""

    @staticmethod
    def validate_required_keys(data: dict[str, Any], required_keys: list[str]) -> tuple[bool, list[str]]:
        """Validate presence of mandatory keys in dictionary."""
        missing = [k for k in required_keys if k not in data]
        return len(missing) == 0, missing
