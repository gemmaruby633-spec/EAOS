"""Unit tests for knowledge/ package."""

from __future__ import annotations

from pathlib import Path

from knowledge.evidence.evidence_ledger import EvidenceLedgerEngine
from knowledge.knowledge_base_engine import EAOSKnowledgeBaseEngine
from knowledge.ontology.ontology_reasoner import OntologyReasonerEngine


def test_ontology_reasoner_engine() -> None:
    """Test ontology concept alignment reasoning."""
    reasoner = OntologyReasonerEngine()
    mapping = reasoner.align_concepts("BusinessCapability", "Service")
    assert mapping.relationship == "equivalent_to"
    assert mapping.confidence_score == 1.0


def test_evidence_ledger_engine(tmp_path: Path) -> None:
    """Test auditing evidence ledger entries."""
    engine = EvidenceLedgerEngine(workspace_root=tmp_path)
    ledger = engine.audit_evidence_ledger()

    assert len(ledger) >= 1
    assert ledger[0].evidence_id == "evi-001"


def test_knowledge_base_engine_summary(tmp_path: Path) -> None:
    """Test master knowledge base engine summary generation."""
    ont_dir = tmp_path / "knowledge" / "ontologies"
    ont_dir.mkdir(parents=True, exist_ok=True)
    (ont_dir / "enterprise_ontology.jsonld").write_text('{"@context": {}}')

    engine = EAOSKnowledgeBaseEngine(workspace_root=tmp_path)
    summary = engine.get_knowledge_summary()

    assert summary.axioms_count >= 2
    assert summary.evidence_entries_count >= 1
    assert summary.ontologies_count >= 1
    assert summary.reasoner_active is True
    assert summary.knowledge_base_integrity is True
