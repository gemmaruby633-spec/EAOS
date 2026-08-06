"""DSL v1 Semantic Validator and IR Compiler Adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from packages.business_architecture.domain.meta_model import (
    AttributeMeta,
    EnterpriseMetaModel,
    EntityMeta,
    EventMeta,
    PolicyMeta,
)
from packages.business_architecture.domain.symbol_table import (
    SymbolEntry,
    SymbolTable,
)
from packages.solution_architecture.domain.enterprise_ir import (
    EnterpriseIRGraph,
    IREdge,
    IRNode,
    IRNodeType,
)


class DSLSemanticValidatorAdapter:
    """Adapter validating Enterprise DSL v1 and building IR Graph."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()

    async def parse_and_validate_dsl(
        self, yaml_content: str
    ) -> tuple[EnterpriseMetaModel, SymbolTable, EnterpriseIRGraph]:
        data: dict[str, Any] = yaml.safe_load(yaml_content) or {}
        ent_data = data.get("enterprise", {})

        name = str(ent_data.get("name", "EAOS"))
        version = str(ent_data.get("version", "1.0.0"))
        caps = [str(c) for c in ent_data.get("capabilities", [])]

        entities: list[EntityMeta] = []
        for e_name, e_body in ent_data.get("entities", {}).items():
            attrs = [AttributeMeta(name=k, type_name=str(v)) for k, v in e_body.get("fields", {}).items()]
            entities.append(EntityMeta(name=e_name, attributes=attrs))

        policies = [
            PolicyMeta(policy_id=f"POL-00{i}", statement=str(p))
            for i, p in enumerate(ent_data.get("policies", []), start=1)
        ]

        events = [EventMeta(name=str(ev)) for ev in ent_data.get("events", [])]

        meta = EnterpriseMetaModel(
            version=version,
            enterprise_name=name,
            capabilities=caps,
            entities=entities,
            policies=policies,
            events=events,
        )

        symbols = self._build_symbol_table(meta)
        ir_graph = self._compile_ir_graph(meta)

        return meta, symbols, ir_graph

    def _build_symbol_table(self, meta: EnterpriseMetaModel) -> SymbolTable:
        symbols: dict[str, SymbolEntry] = {}

        for c in meta.capabilities:
            symbols[c] = SymbolEntry(symbol_name=c, category="CAPABILITY")

        for e in meta.entities:
            symbols[e.name] = SymbolEntry(symbol_name=e.name, category="ENTITY")

        for p in meta.policies:
            symbols[p.policy_id] = SymbolEntry(symbol_name=p.policy_id, category="POLICY")

        for ev in meta.events:
            symbols[ev.name] = SymbolEntry(symbol_name=ev.name, category="EVENT")

        return SymbolTable(symbols=symbols)

    def _compile_ir_graph(self, meta: EnterpriseMetaModel) -> EnterpriseIRGraph:
        nodes: list[IRNode] = []
        edges: list[IREdge] = []

        root_node = IRNode(
            node_id=meta.enterprise_name,
            node_type=IRNodeType.ENTERPRISE,
            label=meta.enterprise_name,
        )
        nodes.append(root_node)

        for c in meta.capabilities:
            cid = f"cap-{c}"
            nodes.append(
                IRNode(
                    node_id=cid,
                    node_type=IRNodeType.CAPABILITY,
                    label=c,
                )
            )
            edges.append(
                IREdge(
                    source_id=meta.enterprise_name,
                    target_id=cid,
                    relationship="HAS_CAPABILITY",
                )
            )

        for e in meta.entities:
            eid = f"ent-{e.name}"
            nodes.append(
                IRNode(
                    node_id=eid,
                    node_type=IRNodeType.ENTITY,
                    label=e.name,
                )
            )

        return EnterpriseIRGraph(nodes=nodes, edges=edges)
