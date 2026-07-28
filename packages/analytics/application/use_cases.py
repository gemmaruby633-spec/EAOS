"""Application use cases for Business Analytics and Health Scoring."""

import uuid
from typing import Any

from packages.analytics.domain.models import (
    AnalyticsTrendPoint,
    BusinessKPISnapshot,
)


class CalculateBusinessHealthUseCase:
    """Use case aggregating business metrics into executive snapshot."""

    def execute(self, traffic: int, customers: int, revenue: float, cost: float) -> BusinessKPISnapshot:
        """Calculates conversion rate and ROI percentage."""
        snap_id = f"SNAP-{uuid.uuid4().hex[:8].upper()}"
        conversion = (customers / traffic) if traffic > 0 else 0.0
        roi = ((revenue - cost) / cost * 100.0) if cost > 0 else 0.0
        return BusinessKPISnapshot(
            snapshot_id=snap_id,
            monthly_traffic=traffic,
            conversion_rate=round(conversion, 4),
            net_revenue_usd=round(revenue - cost, 2),
            roi_percentage=round(roi, 2),
        )


class ComputeSystemHealthUseCase:
    """Legacy/DDD use case calculating architectural system health."""

    def execute(
        self,
        system_id: str = "SYS-001",
        metric_value: float = 0.0,
        metrics: dict[str, Any] | None = None,
    ) -> BusinessKPISnapshot:
        """Executes system health computation returning metric snapshot."""
        snap_id = f"MET-{uuid.uuid4().hex[:8].upper()}"
        point = AnalyticsTrendPoint(value=metric_value)
        return BusinessKPISnapshot(
            snapshot_id=snap_id,
            system_id=system_id,
            trends=[point],
        )
