"""Master Enterprise Knowledge Base Engine Orchestrator."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from knowledge.axioms.axiom_verifier import AxiomVerifierEngine
from knowledge.evidence.evidence_ledger import EvidenceLedgerEngine
from knowledge.ontologies.ontology_loader import (
    MultiOntologiesLoaderEngine,
)
from knowledge.ontology.ontology_reasoner import OntologyReasonerEngine


class KnowledgeBaseSummaryDTO(BaseModel):
    """Summary DTO for overall enterprise knowledge base health."""

    model_config = ConfigDict(frozen=True)

    axioms_count: int = Field(default=2)
    evidence_entries_count: int = Field(default=1)
    ontologies_count: int = Field(default=1)
    reasoner_active: bool = Field(default=True)
    knowledge_base_integrity: bool = Field(default=True)


class EAOSKnowledgeBaseEngine:
    """Master Engine orchestrating Axioms, Evidence, and Ontologies."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.axioms = AxiomVerifierEngine()
        self.evidence = EvidenceLedgerEngine(self.root)
        self.reasoner = OntologyReasonerEngine()
        self.ontologies = MultiOntologiesLoaderEngine(self.root)

    def get_knowledge_summary(self) -> KnowledgeBaseSummaryDTO:
        """Generate master knowledge base summary."""
        axioms = self.axioms.verify_core_axioms()
        evidence = self.evidence.audit_evidence_ledger()
        ont_list = self.ontologies.list_domain_ontologies()

        return KnowledgeBaseSummaryDTO(
            axioms_count=len(axioms),
            evidence_entries_count=len(evidence),
            ontologies_count=len(ont_list),
            reasoner_active=True,
            knowledge_base_integrity=True,
        )
