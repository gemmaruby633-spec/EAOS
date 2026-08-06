"""Unit tests for ecosystem/ package."""

from __future__ import annotations

from ecosystem.ecosystem_engine import EAOSEcosystemEngine
from ecosystem.trust.verifier import EcosystemTrustVerifier


def test_ecosystem_trust_verifier() -> None:
    """Test enterprise node trust verification."""
    verifier = EcosystemTrustVerifier()
    attestation = verifier.verify_enterprise_trust("ent-node-01")

    assert attestation.is_verified is True
    assert "zkp_proof" in attestation.proof_hash


def test_ecosystem_engine_summary() -> None:
    """Test master ecosystem engine summary generation."""
    engine = EAOSEcosystemEngine()
    summary = engine.get_ecosystem_summary()

    assert summary.total_member_nodes >= 1
    assert summary.total_published_capabilities >= 1
    assert summary.trust_verification_passed is True
    assert summary.members[0].enterprise_id == "ent-node-01"
