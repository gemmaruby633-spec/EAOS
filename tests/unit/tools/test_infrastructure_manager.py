"""Unit tests for Infrastructure Manager Engine."""

from __future__ import annotations

from pathlib import Path

from tools.validate.infrastructure_manager import (
    InfrastructureManagerEngine,
)


def test_infrastructure_manager_audit(tmp_path: Path) -> None:
    """Test auditing IaC manifests."""
    compose_file = tmp_path / "infra" / "compose" / "docker-compose.yml"
    compose_file.parent.mkdir(parents=True, exist_ok=True)
    compose_file.write_text("version: '3.8'")

    engine = InfrastructureManagerEngine(workspace_root=tmp_path)
    manifests = engine.audit_iac_manifests()

    assert len(manifests) >= 7
    compose_dto = next(m for m in manifests if m.manifest_id == "docker-compose")
    assert compose_dto.is_present is True


def test_purge_misplaced_and_inits(tmp_path: Path) -> None:
    """Test purging misplaced package folders and inits from infra/."""
    misplaced = tmp_path / "infra" / "compose" / "packages"
    misplaced.mkdir(parents=True, exist_ok=True)

    engine = InfrastructureManagerEngine(workspace_root=tmp_path)
    purged = engine.purge_misplaced_and_inits()

    assert purged >= 1
    assert not misplaced.exists()
