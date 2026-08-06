"""Knowledge Application Service orchestrating architecture knowledge graph use cases."""

from packages.knowledge_architecture.domain.models import (
    EnterpriseGraphTopology,
    KnowledgeNode,
    NodeCategory,
)
from packages.knowledge_architecture.ports.knowledge_port import KnowledgeServicePort


class KnowledgeApplicationService:
    """Application Service for Knowledge Architecture domain."""

    def __init__(self, port: KnowledgeServicePort) -> None:
        """Inject KnowledgeServicePort dependency."""
        self._port = port

    async def get_topology_summary(self) -> EnterpriseGraphTopology:
        """Fetch topology summary through the knowledge port."""
        return await self._port.get_topology_summary()

    async def get_nodes_by_category(self, category: NodeCategory) -> list[KnowledgeNode]:
        """Fetch nodes filtered by category."""
        return await self._port.get_nodes_by_category(category)

    async def get_node_lineage(self, node_id: str, depth: int = 3) -> EnterpriseGraphTopology:
        """Fetch lineage graph topology starting from target node ID up to depth."""
        return await self._port.get_node_lineage(node_id, depth=depth)

    async def check_health(self) -> bool:
        """Check status and health of knowledge graph backend engine."""
        return await self._port.check_health()
