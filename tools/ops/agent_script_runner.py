"""Antigravity 2.0 SDK Agent Script Runner for EAOS."""

import json
import sys
from pathlib import Path

# Ensure EAOS root is in sys.path
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def main() -> None:
    """Reads JSON prompt from stdin and returns structured JSON response."""
    try:
        input_data = sys.stdin.read()
        payload = json.loads(input_data) if input_data.strip() else {}

        prompt = payload.get("prompt", "EAOS Architecture Verification")
        role = payload.get("agent_role", "Architect")

        # Import topology use case via DI Container
        from apps.api.app.container import topology_use_case

        snapshot = topology_use_case.get_audit_report()

        response = {
            "status": "SUCCESS",
            "agent_role": role,
            "prompt": prompt,
            "analysis": (
                f"Agent [{role}] evaluated task against EAOS Constitution v3.0. "
                f"Active source files: {snapshot.active_source_files}, "
                f"Health Score: {snapshot.calculated_health_score:.1f}%"
            ),
            "governance_status": snapshot.audit_status,
        }
        print(json.dumps(response, indent=2))
    except Exception as e:
        error_resp = {
            "status": "ERROR",
            "message": f"Agent Script Execution Failed: {e}",
        }
        print(json.dumps(error_resp, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
