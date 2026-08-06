"""Unit tests for PackageRepositoryScanner."""

from __future__ import annotations

from pathlib import Path

from tools.validate.repository_package_scanner import (
    PackageRepositoryScanner,
)


def test_repository_package_scanner(tmp_path: Path) -> None:
    """Test scanner provisions missing __init__.py and README.md."""
    pkg_dir = tmp_path / "packages" / "sample_domain" / "domain"
    pkg_dir.mkdir(parents=True, exist_ok=True)
    (pkg_dir / "models.py").write_text("class Model: pass")

    app_dir = tmp_path / "apps" / "sample_app"
    app_dir.mkdir(parents=True, exist_ok=True)

    scanner = PackageRepositoryScanner(root_dir=tmp_path)
    res = scanner.scan_and_provision()

    assert res["added_inits"] >= 1
    assert res["added_readmes"] >= 1
    assert res["added_configs"] >= 1
    assert (pkg_dir / "__init__.py").exists()
    assert (tmp_path / "packages" / "sample_domain" / "README.md").exists()
    assert (app_dir / "README.md").exists()
    assert (app_dir / "pyproject.toml").exists()
