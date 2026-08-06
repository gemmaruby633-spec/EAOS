"""Unit tests for Generated Artifacts Manager."""

from __future__ import annotations

from pathlib import Path

from tools.validate.generated_artifacts_manager import (
    GeneratedArtifactsManager,
)


def test_time_machine_snapshots_listing(tmp_path: Path) -> None:
    """Test listing canonical time machine snapshots."""
    tm_dir = tmp_path / "generated" / "architecture" / "time_machine"
    tm_dir.mkdir(parents=True, exist_ok=True)
    (tm_dir / "snapshot_prod_baseline_v1.json").write_text('{"ver": "1"}')

    manager = GeneratedArtifactsManager(workspace_root=tmp_path)
    snapshots = manager.list_time_machine_snapshots()

    assert len(snapshots) == 1
    assert snapshots[0].file_name == "snapshot_prod_baseline_v1.json"
    assert snapshots[0].is_canonical is True


def test_purge_invalid_inits(tmp_path: Path) -> None:
    """Test purging invalid __init__.py from non-python generated dirs."""
    gen_dir = tmp_path / "generated" / "docs" / "archive"
    gen_dir.mkdir(parents=True, exist_ok=True)
    init_file = gen_dir / "__init__.py"
    init_file.write_text("# Invalid init")

    manager = GeneratedArtifactsManager(workspace_root=tmp_path)
    purged = manager.purge_invalid_inits()

    assert purged == 1
    assert not init_file.exists()
