"""AST Fitness Functions Inspector Adapter."""

from __future__ import annotations

import ast
from pathlib import Path

from packages.governance.domain.ast_fitness_models import (
    ASTFitnessReport,
    ASTFitnessViolation,
)
from packages.governance.ports.ast_fitness_port import (
    ASTFitnessInspectorPort,
)


class ASTFitnessInspectorAdapter(ASTFitnessInspectorPort):
    """Adapter performing AST analysis on Python domain layers."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()
        self.forbidden_imports = {
            "fastapi",
            "httpx",
            "sqlalchemy",
            "requests",
        }

    async def inspect_repository(self, target_dir: str = "packages") -> ASTFitnessReport:
        scan_path = (self.root / target_dir).resolve()
        if not scan_path.exists():
            return ASTFitnessReport(score=100.0, passed=True)

        violations: list[ASTFitnessViolation] = []
        files_count = 0

        for py_file in scan_path.rglob("*.py"):
            if "domain" not in py_file.parts:
                continue
            files_count += 1
            violations.extend(self._inspect_file(py_file))

        score = max(0.0, 100.0 - (len(violations) * 10.0))
        passed = score >= 80.0 and len(violations) == 0

        return ASTFitnessReport(
            score=score,
            total_files_scanned=files_count,
            violations=violations,
            passed=passed,
        )

    def _inspect_file(self, py_file: Path) -> list[ASTFitnessViolation]:
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
                for alias in node.names:
                    pkg_name = alias.name.split(".")[0]
                    if pkg_name in self.forbidden_imports:
                        violations.append(
                            ASTFitnessViolation(
                                file_path=rel_file,
                                line_number=node.lineno,
                                rule_id="R01-DOMAIN-PURITY",
                                message=(f"Forbidden import '{alias.name}' in domain layer."),
                            )
                        )
            elif isinstance(node, ast.ImportFrom):
                mod = node.module.split(".")[0] if node.module else ""
                if mod in self.forbidden_imports:
                    violations.append(
                        ASTFitnessViolation(
                            file_path=rel_file,
                            line_number=node.lineno,
                            rule_id="R01-DOMAIN-PURITY",
                            message=(f"Forbidden import from '{node.module}' in domain layer."),
                        )
                    )
        return violations
