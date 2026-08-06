"""Mô hình DTO cho hệ thống Schema Doanh nghiệp (SCHEMAS)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class SchemaType(StrEnum):
    """Phân loại Schema."""

    API = "API"
    COMPILER = "COMPILER"
    EVENTS = "EVENTS"
    KNOWLEDGE = "KNOWLEDGE"
    REPRESENTATION = "REPRESENTATION"
    STORAGE = "STORAGE"


@dataclass(frozen=True)
class SchemaDefinition:
    """Thông tin bản ghi Schema."""

    schema_id: str
    version: str
    schema_type: SchemaType
    raw_json: str


@dataclass
class SchemaValidationResult:
    """Kết quả kiểm tra tuân thủ Schema."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    proof_hash: str = ""
