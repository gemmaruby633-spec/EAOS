"""Unit test suite for Phase 3: Enterprise Model Compiler."""

from __future__ import annotations

from pathlib import Path

import pytest
from packages.business_architecture.adapters.change_propagation_adapter import (
    ChangePropagationAdapter,
)
from packages.business_architecture.adapters.yaml_spec_parser_adapter import (
    YAMLBusinessSpecParserAdapter,
)
from packages.solution_architecture.adapters.multi_target_generator_adapter import (
    MultiTargetGeneratorAdapter,
)

SAMPLE_YAML_SPEC = """
capability: sales_discount
policy:
  id: POL-GOLD-001
  name: Gold Customer Discount
decision:
  rules:
    - conditions:
        - field: customer_tier
          operator: equals
          value: GOLD
      discount_percentage: 25.0
      maximum_discount: 3000000.0
      currency: VND
"""


@pytest.mark.anyio
async def test_yaml_spec_parser_and_ir() -> None:
    """Test parsing YAML specification into IR."""
    parser = YAMLBusinessSpecParserAdapter()
    ir = await parser.parse_yaml_spec(SAMPLE_YAML_SPEC)

    assert ir.capability_id == "sales_discount"
    assert ir.policy_id == "POL-GOLD-001"
    assert len(ir.rules) == 1
    assert ir.rules[0].discount_percentage == 25.0


@pytest.mark.anyio
async def test_multi_target_generator(tmp_path: Path) -> None:
    """Test compiling IR into 4 target artifacts."""
    parser = YAMLBusinessSpecParserAdapter(workspace_root=tmp_path)
    generator = MultiTargetGeneratorAdapter()
    propagation = ChangePropagationAdapter(workspace_root=tmp_path)

    ir = await parser.parse_yaml_spec(SAMPLE_YAML_SPEC)
    compilation = await generator.generate_artifacts(ir)

    assert len(compilation.artifacts) == 4
    targets = [a.target_name for a in compilation.artifacts]
    assert "python" in targets
    assert "rego" in targets
    assert "openapi" in targets
    assert "pytest" in targets

    matrix = await propagation.analyze_impact(None, ir, compilation)
    assert matrix.capability_id == "sales_discount"
    assert len(matrix.affected_artifacts) == 4

    written = await propagation.apply_propagation(compilation)
    assert written == 4
