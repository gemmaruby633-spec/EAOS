"""Unit tests for assets/ package."""

from __future__ import annotations

from pathlib import Path

from assets.diagrams.diagram_manager import DiagramManager
from assets.logos.asset_loader import VisualAssetLoader
from assets.templates.template_engine import ArchitectureTemplateEngine


def test_diagram_manager_loader(tmp_path: Path) -> None:
    """Test loading diagram assets."""
    manager = DiagramManager(workspace_root=tmp_path)
    diag = manager.load_diagram("system_architecture_overview.mermaid")
    assert diag.diagram_id == "system_architecture_overview"
    assert "graph TD" in diag.content or "EAOS" in diag.content


def test_visual_asset_loader(tmp_path: Path) -> None:
    """Test loading visual SVG assets."""
    loader = VisualAssetLoader(workspace_root=tmp_path)
    asset = loader.load_svg_asset("logos", "eaos_logo.svg")
    assert asset.asset_type == "SVG"
    assert "<svg>" in asset.svg_content


def test_architecture_template_engine(tmp_path: Path) -> None:
    """Test document template rendering."""
    engine = ArchitectureTemplateEngine(workspace_root=tmp_path)
    rendered = engine.render_template("architecture_document_template", {"TITLE": "EAOS Architecture"})
    assert isinstance(rendered, str)
    assert len(rendered) > 0
