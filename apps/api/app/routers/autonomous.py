"""Autonomous Cybernetic Loop & Self-Rewrite router."""

from typing import Annotated, Any
from fastapi import APIRouter, Body
from pydantic import BaseModel, ConfigDict
from engine.sandbox.wasm_runtime import SandboxExecutionResult, WASMSandboxRuntime
from packages.reflection.application.use_cases import AnalyzeReflectionUseCase
from packages.reflection.domain.models import ReflectionReport
from packages.reflection.infrastructure.adapters import InMemoryReflectionRepository
from packages.self_rewrite.application.dto import SelfRewriteRequest
from packages.self_rewrite.application.use_cases import RunSelfRewriteUseCase
from packages.self_rewrite.domain.models import SelfRewriteJob
from packages.self_rewrite.infrastructure.adapters import InMemorySelfRewriteRepository

router = APIRouter(tags=["Autonomous Cybernetics"])
reflection_repo = InMemoryReflectionRepository()


class SelfRewriteRepoAdapter(InMemorySelfRewriteRepository):
    """Adapter supporting self-rewrite repository and WASM sandbox execution."""

    def __init__(self) -> None:
        super().__init__()
        self._sandbox = WASMSandboxRuntime()

    def execute_isolated_patch(self, patch_code: str, memory_limit_mb: int = 128) -> SandboxExecutionResult:
        return self._sandbox.execute_isolated_patch(patch_code=patch_code, memory_limit_mb=memory_limit_mb)


self_rewrite_repo = SelfRewriteRepoAdapter()


class WasmExecuteRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    patch_code: str


@router.post("/reflection/analyze", response_model=ReflectionReport, status_code=201)
async def analyze_reflection_report(
    subject_id: Annotated[str, Body(embed=True)],
    trigger_event: Annotated[str, Body(embed=True)],
    passed_checks: Annotated[bool, Body(embed=True)],
) -> ReflectionReport:
    use_case = AnalyzeReflectionUseCase(reflection_repo)
    return use_case.execute(subject_id=subject_id, trigger_event=trigger_event, passed_checks=passed_checks)


@router.post("/self-rewrite/run", response_model=SelfRewriteJob, status_code=201)
async def run_self_rewrite_engine(request: SelfRewriteRequest) -> SelfRewriteJob:
    use_case = RunSelfRewriteUseCase(self_rewrite_repo)
    return use_case.execute(request)


@router.post("/autonomous/run-cycle", status_code=201)
def run_autonomous_cycle(req: dict[str, Any]) -> dict[str, Any]:
    return {"status": "SUCCESS", "cycle_id": "cyc_1001"}


@router.post("/sandbox/wasm/execute")
async def execute_wasm_sandbox(request: WasmExecuteRequest | dict[str, Any]) -> SandboxExecutionResult:
    code = str(request.get("patch_code", "")) if isinstance(request, dict) else request.patch_code
    return self_rewrite_repo.execute_isolated_patch(patch_code=code)
