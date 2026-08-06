"""Động cơ xử lý và xếp thứ tự ưu tiên Epics."""

from __future__ import annotations

from epics.models import EpicStatus, PortfolioEpic, WSJFScore


class EpicEngine:
    """Động cơ quản lý và tối ưu hóa Portfolio Epics."""

    def __init__(self) -> None:
        self._epics: dict[str, PortfolioEpic] = {}

    def register_epic(
        self,
        epic_id: str,
        title: str,
        owner: str,
        wsjf: WSJFScore,
    ) -> PortfolioEpic:
        """Đăng ký Epic mới vào hệ thống."""
        epic = PortfolioEpic(
            epic_id=epic_id,
            title=title,
            owner=owner,
            wsjf=wsjf,
            status=EpicStatus.FUNNEL,
        )
        self._epics[epic_id] = epic
        return epic

    def get_prioritized_backlog(self) -> list[PortfolioEpic]:
        """Sắp xếp danh sách Epic theo thứ tự WSJF giảm dần."""
        return sorted(
            self._epics.values(),
            key=lambda e: e.wsjf.score,
            reverse=True,
        )

    def transition_status(
        self,
        epic_id: str,
        new_status: EpicStatus,
    ) -> PortfolioEpic:
        """Chuyển đổi trạng thái vòng đời Epic."""
        if epic_id not in self._epics:
            raise KeyError(f"Epic {epic_id} không tồn tại.")
        epic = self._epics[epic_id]
        epic.status = new_status
        return epic
