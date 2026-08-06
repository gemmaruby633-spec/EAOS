"""Domain Port interface for Knowledge Architecture Service."""

from typing import Protocol, runtime_checkable

from packages.knowledge_architecture.domain.models import (
    EnterpriseGraphTopology,
    KnowledgeNode,
    NodeCategory,
)


@runtime_checkable
class KnowledgeServicePort(Protocol):
    """Port contract for Knowledge Architecture Graph operations."""

    async def get_topology_summary(self) -> EnterpriseGraphTopology:
        """Retrieve a summary of the enterprise graph topology."""
        ...

    async def get_nodes_by_category(self, category: NodeCategory) -> list[KnowledgeNode]:
        """Retrieve all knowledge nodes belonging to a specific category."""
        ...

    async def get_node_lineage(self, node_id: str, depth: int = 3) -> EnterpriseGraphTopology:
        """Retrieve graph lineage up to specified depth starting from a target node."""
        ...

    async def check_health(self) -> bool:
        """Check connectivity and health status of underlying graph engine."""
        ...
