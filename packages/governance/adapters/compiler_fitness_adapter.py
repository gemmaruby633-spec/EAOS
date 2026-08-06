"""Compiler Architectural Fitness Rules Inspector Adapter."""

from __future__ import annotations

import ast
from pathlib import Path

from packages.governance.domain.ast_fitness_models import (
    ASTFitnessReport,
    ASTFitnessViolation,
)


class CompilerFitnessInspectorAdapter:
    """Inspector enforcing compiler-specific architectural rules."""

    FORBIDDEN_PARSER_MODULES = (
        "yaml_spec_parser",
        "packages.business_architecture.adapters.yaml_spec_parser_adapter",
    )

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    async def inspect_compiler_architecture(self) -> ASTFitnessReport:
        gen_dir = self.root / "packages" / "solution_architecture" / "adapters"

        py_files = list(gen_dir.glob("*generator*.py")) if gen_dir.exists() else []

        violations: list[ASTFitnessViolation] = []
        for py_file in py_files:
            violations.extend(self._inspect_generator_file(py_file))

        score = max(0.0, 100.0 - (len(violations) * 15.0))
        passed = score >= 80.0 and len(violations) == 0

        return ASTFitnessReport(
            score=score,
            total_files_scanned=len(py_files),
            violations=violations,
            passed=passed,
        )

    def _inspect_generator_file(self, py_file: Path) -> list[ASTFitnessViolation]:
        violations: list[ASTFitnessViolation] = []
        try:
            tree = ast.parse(
                py_file.read_text(encoding="utf-8"),
                filename=str(py_file),
            )
        except SyntaxError:
            return violations

        rel_file = str(py_file.relative_to(self.root))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                violations.extend(
                    [
                        ASTFitnessViolation(
                            file_path=rel_file,
                            line_number=node.lineno,
                            rule_id="CR01-GENERATOR-NO-PARSER",
                            message=(f"Forbidden import '{alias.name}' in generator."),
                        )
                        for alias in node.names
                        if alias.name in self.FORBIDDEN_PARSER_MODULES
                        or any(alias.name.startswith(mod + ".") for mod in self.FORBIDDEN_PARSER_MODULES)
                    ]
                )
            elif isinstance(node, ast.ImportFrom) and node.module:
                mod_name = node.module
                is_forbidden = mod_name in self.FORBIDDEN_PARSER_MODULES or any(
                    mod_name.startswith(m + ".") for m in self.FORBIDDEN_PARSER_MODULES
                )
                if is_forbidden:
                    violations.append(
                        ASTFitnessViolation(
                            file_path=rel_file,
                            line_number=node.lineno,
                            rule_id="CR01-GENERATOR-NO-PARSER",
                            message=(f"Forbidden import from '{mod_name}' in generator."),
                        )
                    )
        return violations
