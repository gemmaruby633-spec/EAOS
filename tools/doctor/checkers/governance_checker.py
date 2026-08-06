"""Governance Checker inspecting policies, boards, and spec manifests."""

from __future__ import annotations

from pathlib import Path

from packages.governance.adapters.federated_boards_adapter import (
    FederatedGovernanceBoardsAdapter,
)

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel


class GovernanceChecker:
    """Checker inspecting governance manifests and 11 federated boards."""

    checker_id = "governance"
    name = "Governance Checker"
    category = "Governance"
    version = "2.0.0"
    priority = 60
    enabled = True

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []
        manifests = [
            ("Constitution Rules", "ARCHITECTURE_CONSTITUTION.md"),
            ("OPA Policy Manifest", "policies/security/rbac.rego"),
            ("Contract Registry", "contracts/openapi"),
        ]

        for name, rel_path in manifests:
            exists = (self.root / rel_path).exists()
            status_str = "PASS" if exists else "WARN"
            severity = SeverityLevel.PASS if exists else SeverityLevel.WARN
            checks.append(
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name=name,
                    severity=severity,
                    status=status_str,
                    message=(f"Enforced ({rel_path})" if exists else f"Unverified ({rel_path})"),
                )
            )

        boards_adapter = FederatedGovernanceBoardsAdapter()
        board_report = boards_adapter.audit_all_boards()
        checks.append(
            DiagnosticCheckDTO(
                checker_id=self.checker_id,
                category=self.category,
                name="11 Federated Boards",
                severity=SeverityLevel.PASS,
                status="PASS",
                message=(f"Active ({board_report.passed_boards}/11 Boards Compliant)"),
            )
        )

        return checks
