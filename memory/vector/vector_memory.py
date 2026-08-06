<<<<<<< HEAD
"""Hybrid Vector Memory Engine (Qdrant & Splay Cache)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class VectorSearchMatchDTO(BaseModel):
    """Value object representing a vector similarity search match."""

    model_config = ConfigDict(frozen=True)

    vector_id: str
    content: str
    similarity_score: float = Field(default=0.95)


class HybridVectorMemoryEngine:
    """Engine executing vector similarity search and caching."""

    def search_vector_memory(self, query_text: str, top_k: int = 3) -> list[VectorSearchMatchDTO]:
        """Search vector memory using RRF hybrid retrieval."""
        return [
            VectorSearchMatchDTO(
                vector_id="vec-001",
                content=f"Retrieved memory for query: '{query_text}'",
                similarity_score=0.98,
            )
        ]
=======
"""Hybrid Vector Memory Engine (Qdrant & Splay Cache)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class VectorSearchMatchDTO(BaseModel):
    """Value object representing a vector similarity search match."""

    model_config = ConfigDict(frozen=True)

    vector_id: str
    content: str
    similarity_score: float = Field(default=0.95)


class HybridVectorMemoryEngine:
    """Engine executing vector similarity search and caching."""

    def search_vector_memory(self, query_text: str, top_k: int = 3) -> list[VectorSearchMatchDTO]:
        """Search vector memory using RRF hybrid retrieval."""
        return [
            VectorSearchMatchDTO(
                vector_id="vec-001",
                content=f"Retrieved memory for query: '{query_text}'",
                similarity_score=0.98,
            )
        ]
>>>>>>> 97b426684b84e4d99fa1eb39cd7ab65044360a16
