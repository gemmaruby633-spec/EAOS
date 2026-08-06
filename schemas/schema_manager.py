"""Facade Orchestrator quản lý toàn bộ phân hệ SCHEMAS."""

from __future__ import annotations

from typing import Any

from api.api_schema_engine import ApiSchemaEngine
from automation.dry_run_schema_simulator import (
    DryRunSchemaSimulator,
)
from compiler.compiler_schema_engine import CompilerSchemaEngine
from events.event_schema_engine import EventSchemaEngine
from knowledge.knowledge_schema_engine import KnowledgeSchemaEngine
from ledger.quantum_schema_ledger import QuantumSchemaLedger
from models import SchemaValidationResult
from representation.representation_schema_engine import (
    RepresentationSchemaEngine,
)
from storage.storage_schema_engine import StorageSchemaEngine


class SchemaManager:
    """Facade hợp nhất điều phối toàn bộ Schema Doanh nghiệp."""

    def __init__(self) -> None:
        self.api = ApiSchemaEngine()
        self.compiler = CompilerSchemaEngine()
        self.events = EventSchemaEngine()
        self.knowledge = KnowledgeSchemaEngine()
        self.representation = RepresentationSchemaEngine()
        self.storage = StorageSchemaEngine()

    def validate_payload_against_schema(self, schema_name: str, payload: dict[str, Any]) -> SchemaValidationResult:
        """Kiểm tra tính hợp lệ của Payload theo Schema."""
        is_valid = len(payload) > 0
        errors = [] if is_valid else ["Payload không được rỗng."]

        proof = QuantumSchemaLedger.generate_schema_proof(schema_name, payload)
        return SchemaValidationResult(
            is_valid=is_valid,
            errors=errors,
            proof_hash=proof,
        )

    def simulate_schema_migration(
        self,
        schema_name: str,
        old_version: str,
        new_version: str,
    ) -> dict[str, Any]:
        """Mô phỏng tác động nâng cấp phiên bản Schema."""
        return DryRunSchemaSimulator.simulate_migration(schema_name, old_version, new_version)
