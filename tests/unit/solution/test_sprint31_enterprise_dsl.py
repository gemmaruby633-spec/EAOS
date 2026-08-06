"""Unit test suite for Sprint 3.1: Enterprise Language & IR."""

from __future__ import annotations

import pytest
from packages.business_architecture.adapters.dsl_semantic_validator import (
    DSLSemanticValidatorAdapter,
)
from packages.solution_architecture.domain.enterprise_ir import IRNodeType

SAMPLE_ENTERPRISE_DSL = """
enterprise:
  name: EAOS
  version: 1.0.0
  capabilities:
    - CustomerManagement
    - KnowledgeManagement
  entities:
    Customer:
      fields:
        id: UUID
        name: string
  policies:
    - CustomerMustBeUnique
  events:
    - CustomerCreated
"""


@pytest.mark.anyio
async def test_dsl_semantic_validator_and_ir_compilation() -> None:
    """Test DSL v1 parsing, symbol table creation, and IR Graph compilation."""
    adapter = DSLSemanticValidatorAdapter()
    meta, symbols, ir = await adapter.parse_and_validate_dsl(SAMPLE_ENTERPRISE_DSL)

    assert meta.enterprise_name == "EAOS"
    assert len(meta.capabilities) == 2
    assert len(meta.entities) == 1
    assert meta.entities[0].name == "Customer"

    assert symbols.contains("CustomerManagement")
    assert symbols.contains("Customer")
    assert symbols.contains("POL-001")
    assert symbols.contains("CustomerCreated")

    assert len(ir.nodes) >= 4
    assert ir.nodes[0].node_type == IRNodeType.ENTERPRISE
    assert len(ir.edges) >= 2
