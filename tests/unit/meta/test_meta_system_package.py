"""Unit tests for meta/ package."""

from __future__ import annotations

from pathlib import Path

from meta.classification.classification_engine import (
    ClassificationLevel,
    DataClassificationEngine,
)
from meta.enterprise_meta_system import EAOSEnterpriseMetaSystem


def test_data_classification_engine() -> None:
    """Test data sensitivity classification."""
    engine = DataClassificationEngine()
    res = engine.classify_field("password")
    assert res.level == ClassificationLevel.CONFIDENTIAL


def test_enterprise_meta_system_summary(tmp_path: Path) -> None:
    """Test master meta-system summary generation."""
    system = EAOSEnterpriseMetaSystem(workspace_root=tmp_path)
    summary = system.get_meta_system_summary()

    assert summary.meta_entities_count >= 1
    assert summary.taxonomies_count >= 2
    assert summary.classification_active is True
