"""Federated Governance Board Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.governance.domain.governance_boards import (
    BoardAuditReportDTO,
    BoardCharterDTO,
    BoardID,
)


@runtime_checkable
class GovernanceBoardPort(Protocol):
    """Port protocol for executing 11-Board Federated Governance."""

    def get_board_charter(self, board_id: BoardID) -> BoardCharterDTO: ...

    def audit_all_boards(self) -> BoardAuditReportDTO: ...
