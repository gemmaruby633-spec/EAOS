"""Động cơ suy luận tri thức."""

from __future__ import annotations


class KnowledgeEngine:
    """Truy vấn tri thức."""

    def query_ontology(self, concept: str) -> bool:
        """Truy vấn khái niệm."""
        return len(concept) > 0
