"""Framework Runtime Loader and Resolver services."""

from pathlib import Path

from packages.frameworks.domain.models import EAFrameworkType
from packages.frameworks.domain.registry import (
    FrameworkConceptVO,
    FrameworkRegistry,
)


class FrameworkResolver:
    """Resolves cross-framework mappings and capability queries."""

    def __init__(self, registry: FrameworkRegistry) -> None:
        self.registry = registry

    def resolve_by_framework(self, framework: EAFrameworkType) -> list[FrameworkConceptVO]:
        """Filters concepts belonging to a specific framework."""
        return [c for c in self.registry.concepts.values() if c.framework == framework]

    def resolve_by_capability(self, capability_id: str) -> list[FrameworkConceptVO]:
        """Finds framework concepts bound to an EAOS Capability."""
        return [c for c in self.registry.concepts.values() if c.mapped_eaos_capability == capability_id]


class FrameworkLoader:
    """Loads and hydrates framework runtime from capability manifests."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()

    def load_runtime_registry(self) -> FrameworkRegistry:
        """Scans workspace and builds active FrameworkRegistry instance."""
        registry = FrameworkRegistry()

        seed_concepts = [
            FrameworkConceptVO(
                concept_id="TOGAF-ADM-A",
                framework=EAFrameworkType.TOGAF,
                name="Architecture Vision",
                category="ADM Phase",
                mapped_eaos_capability="governance",
            ),
            FrameworkConceptVO(
                concept_id="BIZBOK-CAP-01",
                framework=EAFrameworkType.CAPSTERA,
                name="Business Capability Model",
                category="Capability",
                mapped_eaos_capability="marketing",
            ),
            FrameworkConceptVO(
                concept_id="APQC-PCF-1.0",
                framework=EAFrameworkType.CAPSTERA,
                name="Develop and Manage Strategy",
                category="Process Category",
                mapped_eaos_capability="governance",
            ),
        ]

        for concept in seed_concepts:
            registry = registry.register_concept(concept)

        return registry


if __name__ == "__main__":
    loader = FrameworkLoader()
    reg = loader.load_runtime_registry()
    resolver = FrameworkResolver(reg)
    togaf_concepts = resolver.resolve_by_framework(EAFrameworkType.TOGAF)
    print(f"✔ Framework Runtime Loaded: {len(reg.concepts)} concepts.")
    print(f"✔ TOGAF Resolved Concepts: {len(togaf_concepts)}")
