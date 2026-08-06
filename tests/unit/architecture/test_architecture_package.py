"""Unit tests for architecture/ package."""

from __future__ import annotations

from architecture.decisions.adr_manager import ADRManager
from architecture.models.c4_model import C4Element, C4LayerType
from architecture.models.canonical_layers import CanonicalLayerRegistry
from architecture.views.mermaid_exporter import MermaidExporter


def test_adr_manager_list_adrs() -> None:
    """Test listing ratified ADR records."""
    manager = ADRManager()
    adrs = manager.list_adrs()
    assert len(adrs) >= 3
    adr_ids = [a.adr_id for a in adrs]
    assert "ADR-UI-001" in adr_ids


def test_canonical_layers_registry() -> None:
    """Test retrieving 52 canonical layers."""
    reg = CanonicalLayerRegistry()
    layers = reg.get_canonical_layers()
    assert len(layers) >= 4
    assert layers[0].layer_name == "Core Kernel"


def test_mermaid_exporter() -> None:
    """Test exporting C4 elements to Mermaid diagram."""
    exporter = MermaidExporter()
    elem = C4Element(
        element_id="elem-1",
        name="API Gateway",
        layer_type=C4LayerType.CONTAINER,
        technology="FastAPI",
    )
    mmd = exporter.export_c4_diagram([elem])
    assert "graph TD" in mmd
    assert "API Gateway" in mmd
