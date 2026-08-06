"""Aggregate catalog module."""

from __future__ import annotations

from typing import Any


class AggregateCatalogEngine:
    """Aggregate catalog engine."""

    def __init__(self) -> None:
        self.aggregates: dict[str, Any] = {}


AggregateCatalog = AggregateCatalogEngine
