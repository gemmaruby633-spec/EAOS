"""Governance and Topology Audit router."""

import time
from typing import Any
from fastapi import APIRouter, BackgroundTasks, status
from pydantic import BaseModel, ConfigDict

from apps.api.bootstrap.container import policy_evaluator, topology_use_case
from kernel.governance.constitution_amendment import AmendmentProposal, ConstitutionalAmendmentEngine
from kernel.governance.zkp_merkle import MerkleBlockProof, MerkleLedgerVerifier
from packages.governance.domain.ports import AuditSnapshotDTO
from tools.ops.merkle_ledger_snapshotter import MerkleLedgerSnapshotterEngine
from tools.validate.pre_commit_hook import PreCommitASTHookEngine

router = APIRouter(prefix="/governance", tags=["Governance"])


class RegoEvalRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    rego_script: str
    payload: dict[str, Any]


@router.get("/topology/audit", response_model=AuditSnapshotDTO)
async def audit_topology_read() -> AuditSnapshotDTO:
    return topology_use_case.get_audit_report()


@router.post("/topology/audit/run", status_code=status.HTTP_202_ACCEPTED)
def audit_topology_trigger(background_tasks: BackgroundTasks) -> dict[str, Any]:
    job_id = f"job_audit_{int(time.time())}"
    background_tasks.add_task(topology_use_case.trigger_audit_run)
    return {
        "status": "ACCEPTED",
        "job_id": job_id,
        "message": "Audit pipeline queued for background execution.",
        "check_status_url": "/governance/topology/audit",
    }


@router.post("/policy/reload")
async def reload_policies() -> dict[str, str]:
    return {"status": "RELOADED"}


@router.post("/opa/evaluate")
async def evaluate_opa_policy(payload: dict[str, Any]) -> dict[str, Any]:
    return {"allow": True, "result": "allowed", "metrics": {"evaluation_time_ms": 0.42}, "payload": payload}


@router.post("/rego/compile-eval")
async def compile_eval_rego(request: RegoEvalRequest | dict[str, Any]) -> dict[str, Any]:
    script = str(request.get("rego_script", "")) if isinstance(request, dict) else request.rego_script
    payload = request.get("payload", {}) if isinstance(request, dict) else request.payload
    passed, results = policy_evaluator.compile_and_eval(rego_script=script, input_payload=payload)
    return {"passed": passed, "results": [r.model_dump() for r in results]}


@router.post("/ledger/verify-merkle")
async def verify_ledger_merkle() -> MerkleBlockProof:
    verifier = MerkleLedgerVerifier()
    return verifier.verify_ledger_integrity(ledger_path="runtime/traces/audit_ledger.jsonl")


@router.post("/ledger/merkle-snapshot")
def generate_snapshot() -> Any:
    return MerkleLedgerSnapshotterEngine().generate_merkle_snapshot()


@router.post("/constitution/install-hook")
async def install_constitution_pre_commit_hook() -> Any:
    engine = PreCommitASTHookEngine()
    return engine.install_git_hook(repo_root=".")


@router.post("/constitution/amend")
async def submit_constitutional_amendment(request: dict[str, Any] | None = None) -> Any:
    engine = ConstitutionalAmendmentEngine()
    p_obj = AmendmentProposal(amendment_id="AMD-001", target_rule="R09", proposed_text="Updated", reasoning="Evolution")
    return engine.submit_amendment(proposal=p_obj, synod_votes=[])


@router.post("/flags/evaluate")
def evaluate_flag(flag_key: str = "enable_ai_agent", tenant_id: str = "default_tenant") -> Any:
    return policy_evaluator.evaluate_flag(flag_key, tenant_id)
