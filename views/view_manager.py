"""Facade Orchestrator quản lý toàn bộ phân hệ VIEWS."""

from __future__ import annotations

from typing import Any

from automation.dry_run_view_simulator import (
    DryRunViewSimulator,
)
from eaos.eaos_view_engine import EaosViewEngine
from foundation.foundation_view_engine import (
    FoundationViewEngine,
)
from ledger.quantum_view_ledger import QuantumViewLedger
from library.library_view_engine import LibraryViewEngine
from renderer.mermaid_renderer import MermaidRenderer
from research.research_view_engine import ResearchViewEngine
from runtime.runtime_view_engine import RuntimeViewEngine

from models import RenderResult, ViewFormat


class ViewManager:
    """Facade hợp nhất điều phối 8 phân hệ View Projections."""

    def __init__(self) -> None:
        self.eaos = EaosViewEngine()
        self.foundation = FoundationViewEngine()
        self.library = LibraryViewEngine()
        self.research = ResearchViewEngine()
        self.runtime = RuntimeViewEngine()
        self.mermaid = MermaidRenderer()

    def render_view_projection(self, view_id: str, format_type: ViewFormat = ViewFormat.MERMAID) -> RenderResult:
        """Xuất chiếu View theo định dạng có bằng chứng mã hóa."""
        content = f"graph TD;\n  {view_id}-->Rendered"
        proof = QuantumViewLedger.generate_view_proof(view_id, {"format": format_type.value, "content": content})
        return RenderResult(
            view_id=view_id,
            format=format_type,
            rendered_content=content,
            proof_hash=proof,
        )

    def simulate_view_projection(self, view_id: str, delta: dict[str, Any]) -> dict[str, Any]:
        """Mô phỏng thay đổi View an toàn."""
        return DryRunViewSimulator.simulate_projection(view_id, delta)
