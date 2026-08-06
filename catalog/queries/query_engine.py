"""Động cơ kiểm toán CQRS Queries."""

from __future__ import annotations


class QueryEngine:
    """Xác minh Query handler."""

    def verify_query(self, query_name: str) -> bool:
        """Kiểm tra Query hợp lệ."""
        return query_name.endswith("Query")
