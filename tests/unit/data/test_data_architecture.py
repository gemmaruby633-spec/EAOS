"""Unit tests for data/ package."""

from __future__ import annotations

from data.data_architecture import EAOSDataArchitectureEngine
from data.governance.data_governance import DataGovernanceEngine


def test_data_governance_pii_redaction() -> None:
    """Test PII data redaction in governance engine."""
    gov = DataGovernanceEngine()
    raw = {"email": "user@eaos.internal", "status": "ACTIVE"}
    redacted = gov.redact_pii_data(raw)

    assert redacted["email"] == "[REDACTED_PII]"
    assert redacted["status"] == "ACTIVE"


def test_data_architecture_engine_summary() -> None:
    """Test data architecture summary generation."""
    engine = EAOSDataArchitectureEngine()
    summary = engine.get_architecture_summary()

    assert summary.governance_active is True
    assert summary.lineage_tracked is True
    assert summary.quality_passed is True
