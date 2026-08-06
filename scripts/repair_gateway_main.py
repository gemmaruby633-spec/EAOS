"""Authoritative repair script for apps/api/app/main.py."""

import ast
from pathlib import Path


def repair_gateway() -> None:
    """Rebuilds apps/api/app/main.py with verified AST syntax."""
    main_path = Path("apps/api/app/main.py")
    if not main_path.exists():
        return

    content = main_path.read_text(encoding="utf-8")

    hook_marker = '@app.post("/governance/constitution/install-hook")'
    base_code = content.split(hook_marker)[0].rstrip() if hook_marker in content else content.rstrip()

    top_import_block = (
        "from kernel.governance.constitution_amendment import (\n"
        "    AmendmentProposal,\n"
        "    ConstitutionalAmendmentEngine,\n"
        ")\n"
        "from platforms.telemetry.telemetry_fitness import (\n"
        "    TelemetryFitnessBridge,\n"
        ")\n"
        "from tools.validate.pre_commit_hook import "
        "PreCommitASTHookEngine\n"
    )

    clean_base_lines: list[str] = []
    for line in base_code.splitlines():
        stripped = line.strip()
        if (
            "from tools.validate.pre_commit_hook import" in stripped
            or "from platforms.telemetry.telemetry_fitness import" in stripped
            or "from kernel.governance.constitution_amendment import" in stripped
            or stripped
            in (
                "AmendmentProposal,",
                "ConstitutionalAmendmentEngine,",
                "TelemetryFitnessBridge,",
                "PreCommitASTHookEngine,",
            )
        ):
            continue
        clean_base_lines.append(line)

    clean_base = "\n".join(clean_base_lines)

    tail_routes = """

@app.post("/governance/constitution/install-hook")
async def install_constitution_pre_commit_hook() -> Any:
    engine = PreCommitASTHookEngine()
    return engine.install_git_hook(repo_root=str(ROOT_PATH))


@app.post("/telemetry/fitness-bridge/eval")
async def evaluate_telemetry_fitness_bridge(
    request: dict[str, Any] | None = None,
    trace_metrics: Annotated[
        dict[str, Any] | None, Body(embed=True)
    ] = None,
) -> Any:
    metrics = trace_metrics
    if isinstance(request, dict) and not metrics:
        metrics = request.get("trace_metrics", {})

    bridge = TelemetryFitnessBridge()
    return bridge.process_telemetry_trace(trace_metrics=metrics or {})


@app.post("/governance/constitution/amend")
async def submit_constitutional_amendment(
    request: dict[str, Any] | None = None,
    proposal: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
    synod_votes: Annotated[
        list[dict[str, Any]] | None, Body(embed=True)
    ] = None,
) -> Any:
    prop_data = proposal
    safe_prop = prop_data if isinstance(prop_data, dict) else {}
    votes = synod_votes
    if isinstance(request, dict):
        if not prop_data:
            prop_data = request.get("proposal", {})
        if votes is None:
            votes = request.get("synod_votes", [])

    p_obj = AmendmentProposal(
        amendment_id=str(safe_prop.get("amendment_id", "AMD-001")),
        target_rule=str(safe_prop.get("target_rule", "R09")),
        proposed_text=str(
            safe_prop.get("proposed_text", "Updated Rule")
        ),
        reasoning=str(
            safe_prop.get("reasoning", "Autonomous evolution")
        ),
    )

    engine = ConstitutionalAmendmentEngine()
    return engine.submit_amendment(
        proposal=p_obj, synod_votes=votes or []
    )
"""

    final_code = top_import_block + "\n" + clean_base + tail_routes

    try:
        ast.parse(final_code)
        main_path.write_text(final_code, encoding="utf-8")
        print("✔ Gateway main.py AST syntax repaired 100% successfully.")
    except SyntaxError as err:
        print(f"✖ Syntax error during repair: {err}")


if __name__ == "__main__":
    repair_gateway()
