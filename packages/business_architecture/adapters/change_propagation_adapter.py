"""Business Change Propagation Adapter."""

from __future__ import annotations

from pathlib import Path

from packages.business_architecture.domain.compiler_models import (
    BusinessSpecificationIR,
)
from packages.business_architecture.domain.propagation_models import (
    AffectedArtifact,
    ImpactAnalysisMatrix,
)
from packages.solution_architecture.domain.generator_models import (
    MultiTargetCompilationResult,
)


class ChangePropagationAdapter:
    """Adapter calculating Impact Analysis Matrix for business changes."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()

    async def analyze_impact(
        self,
        old_ir: BusinessSpecificationIR | None,
        new_ir: BusinessSpecificationIR,
        compilation: MultiTargetCompilationResult,
    ) -> ImpactAnalysisMatrix:
        affected: list[AffectedArtifact] = []

        for art in compilation.artifacts:
            fpath = self.root / art.file_path
            status = "MODIFIED" if fpath.exists() else "CREATED"
            affected.append(
                AffectedArtifact(
                    target_name=art.target_name,
                    file_path=art.file_path,
                    change_status=status,
                )
            )

        changed_count = 1
        if (
            old_ir
            and old_ir.rules
            and new_ir.rules
            and (old_ir.rules[0].discount_percentage != new_ir.rules[0].discount_percentage)
        ):
            changed_count += 1

        return ImpactAnalysisMatrix(
            capability_id=new_ir.capability_id,
            policy_id=new_ir.policy_id,
            values_changed_count=changed_count,
            affected_artifacts=affected,
            required_tests_count=len(compilation.artifacts),
        )

    async def apply_propagation(self, compilation: MultiTargetCompilationResult) -> int:
        written_count = 0
        for art in compilation.artifacts:
            out_path = self.root / art.file_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(art.content, encoding="utf-8")
            written_count += 1
        return written_count
