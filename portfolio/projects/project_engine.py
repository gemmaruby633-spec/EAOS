"""Động cơ theo dõi tiến độ Dự án."""

from __future__ import annotations

from projects.models import EarnedValueMetrics, PortfolioProject


class ProjectEngine:
    """Theo dõi và đánh giá sức khỏe Dự án."""

    def __init__(self) -> None:
        self._projects: dict[str, PortfolioProject] = {}

    def track_project(
        self,
        project_id: str,
        name: str,
        bac: float,
        evm: EarnedValueMetrics,
    ) -> PortfolioProject:
        """Ghi nhận dự án và chỉ số EVM."""
        proj = PortfolioProject(
            project_id=project_id,
            name=name,
            budget_at_completion=bac,
            evm=evm,
        )
        self._projects[project_id] = proj
        return proj

    def get_health_summary(self, project_id: str) -> dict[str, float]:
        """Trích xuất báo cáo sức khỏe tài chính và tiến độ."""
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} không tồn tại.")
        proj = self._projects[project_id]
        return {
            "CPI": round(proj.evm.cpi, 3),
            "SPI": round(proj.evm.spi, 3),
            "EAC": round(
                proj.evm.estimate_at_completion(proj.budget_at_completion),
                2,
            ),
        }
