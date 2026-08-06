from __future__ import annotations

from typing import Any

from packages.knowledge_architecture.domain.models import (
    EnterpriseGraphTopology,
    KnowledgeNode,
    KnowledgeRelationship,
    NodeCategory,
    RelationshipType,
)
from packages.knowledge_architecture.ports.knowledge_port import KnowledgeServicePort


class Neo4jKnowledgeAdapter(KnowledgeServicePort):
    """Production-grade Neo4j implementation of KnowledgeServicePort."""

    def __init__(self, driver: Any = None, database: str = "neo4j") -> None:
        self._driver = driver
        self._database = database

    async def check_health(self) -> bool:
        if self._driver is None:
            return True
        try:
            await self._driver.verify_connectivity()
            return True
        except Exception:
            return False

    async def get_topology_summary(self) -> EnterpriseGraphTopology:
        if self._driver is None:
            return EnterpriseGraphTopology()

        query = "MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 500"
        records, _, _ = await self._driver.execute_query(
            query,
            database_=self._database,
        )

        nodes_map: dict[str, KnowledgeNode] = {}
        relationships: list[KnowledgeRelationship] = []

        for record in records:
            raw_n = record.get("n")
            if raw_n:
                node = self._map_node(raw_n)
                nodes_map[node.id] = node

            raw_m = record.get("m")
            if raw_m:
                node_m = self._map_node(raw_m)
                nodes_map[node_m.id] = node_m

            raw_r = record.get("r")
            if raw_r and raw_n and raw_m:
                rel = KnowledgeRelationship(
                    source_id=str(raw_n.get("id", raw_n.element_id)),
                    target_id=str(raw_m.get("id", raw_m.element_id)),
                    relation=RelationshipType(raw_r.type),
                    properties=dict(raw_r.items()),
                )
                relationships.append(rel)

        node_list = list(nodes_map.values())
        return EnterpriseGraphTopology(
            nodes=node_list,
            relationships=relationships,
            total_nodes=len(node_list),
            total_relationships=len(relationships),
        )

    async def get_nodes_by_category(
        self,
        category: NodeCategory,
    ) -> list[KnowledgeNode]:
        if self._driver is None:
            return []

        query = f"MATCH (n:{category.value}) RETURN n"
        records, _, _ = await self._driver.execute_query(
            query,
            database_=self._database,
        )
        return [self._map_node(record["n"]) for record in records if record.get("n")]

    async def get_node_lineage(
        self,
        node_id: str,
        depth: int = 3,
    ) -> EnterpriseGraphTopology:
        if self._driver is None:
            return EnterpriseGraphTopology()

        query = "MATCH path = (start {id: $node_id})-[r*1..3]-(target) RETURN path LIMIT 100"
        records, _, _ = await self._driver.execute_query(
            query,
            node_id=node_id,
            database_=self._database,
        )

        nodes_map: dict[str, KnowledgeNode] = {}
        relationships: list[KnowledgeRelationship] = []

        for record in records:
            path = record.get("path")
            if not path:
                continue
            for node in path.nodes:
                mapped = self._map_node(node)
                nodes_map[mapped.id] = mapped

            relationships.extend(
                [
                    KnowledgeRelationship(
                        source_id=str(rel.start_node.get("id", rel.start_node.element_id)),
                        target_id=str(rel.end_node.get("id", rel.end_node.element_id)),
                        relation=RelationshipType(rel.type),
                        properties=dict(rel.items()),
                    )
                    for rel in path.relationships
                ]
            )

        node_list = list(nodes_map.values())
        return EnterpriseGraphTopology(
            nodes=node_list,
            relationships=relationships,
            total_nodes=len(node_list),
            total_relationships=len(relationships),
        )

    @staticmethod
    def _map_node(raw_node: Any) -> KnowledgeNode:
        labels = list(raw_node.labels)
        category = NodeCategory.CAPABILITY_DOMAIN
        for label in labels:
            if label in NodeCategory.__members__.values():
                category = NodeCategory(label)
                break

        props = dict(raw_node.items())
        node_id = str(props.get("id", raw_node.element_id))
        name = str(props.get("name", node_id))

        return KnowledgeNode(
            id=node_id,
            name=name,
            category=category,
            properties=props,
        )
