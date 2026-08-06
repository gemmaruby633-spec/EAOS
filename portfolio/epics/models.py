"""Mô hình dữ liệu DTO cho Portfolio Epics."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EpicStatus(StrEnum):
    """Trạng thái vòng đời của Portfolio Epic."""

    FUNNEL = "FUNNEL"
    ANALYZING = "ANALYZING"
    BACKLOG = "BACKLOG"
    IMPLEMENTING = "IMPLEMENTING"
    DONE = "DONE"


@dataclass(frozen=True)
class WSJFScore:
    """Điểm số ưu tiên Weighted Shortest Job First."""

    user_value: float
    time_criticality: float
    rroe: float
    job_size: float

    @property
    def cost_of_delay(self) -> float:
        """Tính tổng chi phí hoãn lại (Cost of Delay)."""
        return self.user_value + self.time_criticality + self.rroe

    @property
    def score(self) -> float:
        """Tính chỉ số WSJF."""
        if self.job_size <= 0:
            return 0.0
        return self.cost_of_delay / self.job_size


@dataclass
class PortfolioEpic:
    """Mô hình Epic chuẩn BIZBOK."""

    epic_id: str
    title: str
    owner: str
    wsjf: WSJFScore
    status: EpicStatus = EpicStatus.FUNNEL
