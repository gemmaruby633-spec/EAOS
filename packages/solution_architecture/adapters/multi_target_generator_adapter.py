"""Multi-Target Code Generator Adapter for 4 Targets."""

from __future__ import annotations

from packages.business_architecture.domain.compiler_models import (
    BusinessSpecificationIR,
)
from packages.solution_architecture.domain.generator_models import (
    GeneratedArtifact,
    MultiTargetCompilationResult,
)
from packages.solution_architecture.ports.generator_port import (
    MultiTargetGeneratorPort,
)


class MultiTargetGeneratorAdapter(MultiTargetGeneratorPort):
    """Adapter compiling IR into Python, Rego, OpenAPI, and Pytest."""

    async def generate_artifacts(self, spec_ir: BusinessSpecificationIR) -> MultiTargetCompilationResult:
        py_art = self._generate_python(spec_ir)
        rego_art = self._generate_rego(spec_ir)
        openapi_art = self._generate_openapi(spec_ir)
        pytest_art = self._generate_pytest(spec_ir)

        return MultiTargetCompilationResult(
            capability_id=spec_ir.capability_id,
            policy_id=spec_ir.policy_id,
            artifacts=[py_art, rego_art, openapi_art, pytest_art],
        )

    def _generate_python(self, ir: BusinessSpecificationIR) -> GeneratedArtifact:
        cap = ir.capability_id
        rule = ir.rules[0] if ir.rules else None
        disc = rule.discount_percentage if rule else 0.0
        cap_limit = rule.maximum_discount if rule else 0.0

        content = (
            '"""Auto-generated Python Domain Policy."""\n\n'
            "from decimal import Decimal\n\n\n"
            f"def calculate_{cap}_discount(amount: Decimal) -> Decimal:\n"
            f'    """Calculate discount for {ir.policy_name}."""\n'
            f'    raw = amount * Decimal("{disc / 100.0:.2f}")\n'
            f'    max_cap = Decimal("{cap_limit:.2f}")\n'
            "    return min(raw, max_cap) if max_cap > 0 else raw\n"
        )
        return GeneratedArtifact(
            target_name="python",
            file_path=f"packages/{cap}/domain/discount_policy.py",
            content=content,
        )

    def _generate_rego(self, ir: BusinessSpecificationIR) -> GeneratedArtifact:
        cap = ir.capability_id
        rule = ir.rules[0] if ir.rules else None
        disc = rule.discount_percentage if rule else 0.0

        content = (
            f"# Auto-generated OPA Rego Policy: {ir.policy_id}\n"
            f"package eaos.{cap}\n\n"
            "default allow = false\n\n"
            "allow if {\n"
            '    input.customer_tier == "GOLD"\n'
            f"    input.discount_rate == {disc / 100.0}\n"
            "}\n"
        )
        return GeneratedArtifact(
            target_name="rego",
            file_path=f"policies/{cap}/{ir.policy_id.lower()}.rego",
            content=content,
        )

    def _generate_openapi(self, ir: BusinessSpecificationIR) -> GeneratedArtifact:
        cap = ir.capability_id
        content = (
            f"# Auto-generated OpenAPI 3.1 Spec for {cap}\n"
            "openapi: 3.1.0\n"
            f"info:\n  title: {ir.policy_name}\n  version: 1.0.0\n"
            f"paths:\n  /{cap}/calculate:\n    post:\n"
            f"      summary: Calculate {cap} discount\n"
        )
        return GeneratedArtifact(
            target_name="openapi",
            file_path=f"contracts/openapi/{cap}_v1.yaml",
            content=content,
        )

    def _generate_pytest(self, ir: BusinessSpecificationIR) -> GeneratedArtifact:
        cap = ir.capability_id
        content = (
            f'"""Auto-generated Pytest for {cap}."""\n\n'
            "from decimal import Decimal\n"
            f"from packages.{cap}.domain.discount_policy import (\n"
            f"    calculate_{cap}_discount,\n"
            ")\n\n\n"
            f"def test_calculate_{cap}_discount() -> None:\n"
            f"    res = calculate_{cap}_discount(Decimal('10000000'))\n"
            "    assert res > Decimal('0')\n"
        )
        return GeneratedArtifact(
            target_name="pytest",
            file_path=f"tests/unit/generated/test_{cap}_discount.py",
            content=content,
        )
