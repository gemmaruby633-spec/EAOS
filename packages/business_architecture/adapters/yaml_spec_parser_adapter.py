"""YAML Business Specification Parser Adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from packages.business_architecture.domain.compiler_models import (
    BusinessDecisionRule,
    BusinessSpecificationIR,
    DecisionCondition,
)
from packages.business_architecture.ports.compiler_port import (
    BusinessSpecParserPort,
)


class YAMLBusinessSpecParserAdapter(BusinessSpecParserPort):
    """Adapter parsing YAML business specifications into IR."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()

    async def parse_yaml_spec(self, yaml_content: str) -> BusinessSpecificationIR:
        data: dict[str, Any] = yaml.safe_load(yaml_content) or {}

        capability_id = str(data.get("capability", "unknown_capability"))
        policy_data = data.get("policy", {})
        policy_id = str(policy_data.get("id", "POL-001"))
        policy_name = str(policy_data.get("name", "Default Policy"))

        decision = data.get("decision", {})
        rules_raw = decision.get("rules", [])

        parsed_rules: list[BusinessDecisionRule] = []
        for idx, r in enumerate(rules_raw, start=1):
            conds = [
                DecisionCondition(
                    field=str(c.get("field", "")),
                    operator=str(c.get("operator", "equals")),
                    value=c.get("value"),
                )
                for c in r.get("conditions", [])
            ]
            parsed_rules.append(
                BusinessDecisionRule(
                    rule_id=f"R0{idx}",
                    conditions=conds,
                    discount_percentage=float(r.get("discount_percentage", 0.0)),
                    maximum_discount=float(r.get("maximum_discount", 0.0)),
                    currency=str(r.get("currency", "VND")),
                )
            )

        return BusinessSpecificationIR(
            capability_id=capability_id,
            policy_id=policy_id,
            policy_name=policy_name,
            rules=parsed_rules,
        )

    async def parse_spec_file(self, file_path: str) -> BusinessSpecificationIR:
        path = (self.root / file_path).resolve()
        content = path.read_text(encoding="utf-8")
        return await self.parse_yaml_spec(content)
