"""Unit tests for libs/ package."""

from __future__ import annotations

from libs.crypto.security_utils import CryptographicUtils
from libs.libs_orchestrator import EAOSSharedLibsEngine


def test_cryptographic_utils_sha256() -> None:
    """Test SHA-256 evidence calculation."""
    digest = CryptographicUtils.calculate_sha256("test_payload")
    assert len(digest) == 64
    assert isinstance(digest, str)


def test_shared_libs_engine_evidence() -> None:
    """Test master shared libs engine evidence computation."""
    engine = EAOSSharedLibsEngine()
    res = engine.compute_payload_evidence("hello_eaos")

    assert res.success is True
    assert "digest" in res.data
    assert len(res.data["digest"]) == 64
