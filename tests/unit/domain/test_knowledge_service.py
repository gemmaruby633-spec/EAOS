from __future__ import annotations

import pytest
from packages.knowledge_architecture.application.knowledge_service import (
    KnowledgeApplicationService,
)
from packages.knowledge_architecture.domain.models import (
    EnterpriseGraphTopology,
    KnowledgeNode,
    NodeCategory,
)
from packages.knowledge_architecture.ports.knowledge_port import KnowledgeServicePort


class MockKnowledgeAdapter(KnowledgeServicePort):
    async def check_health(self) -> bool:
        return True

    async def get_topology_summary(self) -> EnterpriseGraphTopology:
        node = KnowledgeNode(
            id="cap-01",
            name="Core Banking Capability",
            category=NodeCategory.CAPABILITY_DOMAIN,
        )
        return EnterpriseGraphTopology(nodes=[node], total_nodes=1)

    async def get_nodes_by_category(self, category: NodeCategory) -> list[KnowledgeNode]:
        return [
            KnowledgeNode(
                id="cap-01",
                name="Core Banking Capability",
                category=category,
            )
        ]

    async def get_node_lineage(self, node_id: str, depth: int = 3) -> EnterpriseGraphTopology:
        if node_id == "cap-01":
            node = KnowledgeNode(
                id="cap-01",
                name="Core Banking Capability",
                category=NodeCategory.CAPABILITY_DOMAIN,
            )
            return EnterpriseGraphTopology(nodes=[node], total_nodes=1)
        return EnterpriseGraphTopology()


@pytest.mark.anyio
async def test_get_topology_summary() -> None:
    adapter = MockKnowledgeAdapter()
    service = KnowledgeApplicationService(port=adapter)
    result = await service.get_topology_summary()
    assert result.total_nodes == 1


@pytest.mark.anyio
async def test_get_nodes_by_category() -> None:
    adapter = MockKnowledgeAdapter()
    service = KnowledgeApplicationService(port=adapter)
    nodes = await service.get_nodes_by_category(NodeCategory.SUB_CAPABILITY)
    assert len(nodes) == 1


@pytest.mark.anyio
async def test_get_node_lineage() -> None:
    adapter = MockKnowledgeAdapter()
    service = KnowledgeApplicationService(port=adapter)
    result = await service.get_node_lineage("cap-01")
    assert result.total_nodes == 1


@pytest.mark.anyio
async def test_check_health() -> None:
    adapter = MockKnowledgeAdapter()
    assert await adapter.check_health() is True
