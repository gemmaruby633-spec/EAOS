"""Multi-Ontologies File Loader Engine (JSON-LD, OWL, TTL)."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class DomainOntologyDTO(BaseModel):
    """Value object representing a domain-specific ontology dataset."""

    model_config = ConfigDict(frozen=True)

    ontology_id: str = Field(..., description="Ontology ID e.g. enterprise")
    file_path: str = Field(..., description="Relative file path")
    format_type: str = Field(default="JSON-LD")
    is_loaded: bool = Field(default=True)


class MultiOntologiesLoaderEngine:
    """Engine loading domain-specific ontologies from knowledge/ontologies/."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.ont_dir = self.root / "knowledge" / "ontologies"

    def list_domain_ontologies(self) -> list[DomainOntologyDTO]:
        """Scan and list all domain ontology dataset files."""
        if not self.ont_dir.exists():
            return []

        results: list[DomainOntologyDTO] = []
        for f in sorted(self.ont_dir.glob("*.*")):
            if f.name.startswith((".", "__")) or f.suffix == ".py":
                continue
            fmt = "JSON-LD" if f.suffix == ".jsonld" else "OWL"
            results.append(
                DomainOntologyDTO(
                    ontology_id=f.stem,
                    file_path=f"knowledge/ontologies/{f.name}",
                    format_type=fmt,
                    is_loaded=True,
                )
            )
        return results
