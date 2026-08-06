"""Unit tests for 11 Federated Governance Boards Adapter."""

from __future__ import annotations

from packages.governance.adapters.federated_boards_adapter import (
    FederatedGovernanceBoardsAdapter,
)
from packages.governance.domain.governance_boards import BoardID


def test_federated_boards_charters_and_audit() -> None:
    """Test auditing all 11 Federated Governance Boards."""
    adapter = FederatedGovernanceBoardsAdapter()
    report = adapter.audit_all_boards()

    assert report.total_boards == 11
    assert report.passed_boards == 11
    assert report.constitutional_compliance is True

    gov_charter = adapter.get_board_charter(BoardID.GOVERNANCE)
    assert gov_charter.board_id == BoardID.GOVERNANCE
    assert "Hiến pháp v3.0" in gov_charter.primary_responsibility
    assert "Constitutional Auditor" in gov_charter.roles_covered
