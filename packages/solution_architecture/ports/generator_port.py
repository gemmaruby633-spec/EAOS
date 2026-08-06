"""Code Generator Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.business_architecture.domain.compiler_models import (
    BusinessSpecificationIR,
)
from packages.solution_architecture.domain.generator_models import (
    MultiTargetCompilationResult,
)


@runtime_checkable
class MultiTargetGeneratorPort(Protocol):
    """Port protocol for compiling IR into 4 target artifacts."""

    async def generate_artifacts(self, spec_ir: BusinessSpecificationIR) -> MultiTargetCompilationResult: ...
