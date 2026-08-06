"""Compiler Semantic Analyzer for DSL v1 (Phase 3)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from packages.business_architecture.domain.meta_model import (
    EnterpriseMetaModel,
)


class SemanticAnalysisReport(BaseModel):
    """Report detailing semantic analysis results."""

    model_config = ConfigDict(frozen=True)

    passed: bool = Field(default=True, description="Analysis pass status")
    errors: list[str] = Field(default_factory=list, description="Semantic errors")
    warnings: list[str] = Field(default_factory=list, description="Semantic warnings")


class SemanticAnalyzer:
    """Analyzer validating semantic integrity of Enterprise Meta-Model."""

    def analyze(self, meta: EnterpriseMetaModel) -> SemanticAnalysisReport:
        errors: list[str] = []
        warnings: list[str] = []

        seen_caps: set[str] = set()
        for cap in meta.capabilities:
            if cap in seen_caps:
                errors.append(f"Duplicate capability detected: '{cap}'")
            seen_caps.add(cap)

        seen_entities: set[str] = set()
        for ent in meta.entities:
            if ent.name in seen_entities:
                errors.append(f"Duplicate entity detected: '{ent.name}'")
            seen_entities.add(ent.name)

        seen_events: set[str] = set()
        for ev in meta.events:
            if ev.name in seen_events:
                errors.append(f"Duplicate event detected: '{ev.name}'")
            seen_events.add(ev.name)

        if not meta.policies:
            warnings.append("No policies defined in enterprise model.")

        passed = len(errors) == 0
        return SemanticAnalysisReport(passed=passed, errors=errors, warnings=warnings)
