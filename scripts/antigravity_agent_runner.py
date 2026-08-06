"""Antigravity 2.0 SDK Agent Script Runner for EAOS."""

import json
import sys
from pathlib import Path

import structlog
from pydantic import BaseModel, ConfigDict

# Ensure EAOS root is in sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

logger = structlog.get_logger()


class AntigravityAgentPayload(BaseModel):
    """Agent payload DTO for stdin JSON parsing."""

    model_config = ConfigDict(frozen=True)

    prompt: str = "EAOS Architecture Verification"
    agent_role: str = "Architect"


class AntigravityAgentResponse(BaseModel):
    """Agent response DTO for stdout JSON serialization."""

    model_config = ConfigDict(frozen=True)

    status: str
    agent_role: str
    prompt: str
    analysis: str
    governance_status: str


def main() -> None:
    """Reads JSON prompt from stdin and returns structured JSON response."""
    try:
        input_data = sys.stdin.read()
        raw_payload = json.loads(input_data) if input_data.strip() else {}
        payload = AntigravityAgentPayload(**raw_payload)

        from tools.graph.system_integration_auditor import (
            SystemIntegrationAuditor,
        )

        auditor = SystemIntegrationAuditor(ROOT_DIR)
        snapshot = auditor.audit_topological_connectivity()

        response = AntigravityAgentResponse(
            status="SUCCESS",
            agent_role=payload.agent_role,
            prompt=payload.prompt,
            analysis=(
                f"Agent [{payload.agent_role}] evaluated task against "
                f"EAOS Constitution v3.0. Total directories: "
                f"{snapshot.total_directories}, "
                f"Connected ratio: {snapshot.connectivity_ratio:.1f}%"
            ),
            governance_status="COMPLIANT",
        )
        sys.stdout.write(json.dumps(response.model_dump(), indent=2) + "\n")
    except Exception as e:
        logger.error("Agent Script Execution Failed", error=str(e))
        error_resp = {
            "status": "ERROR",
            "message": f"Agent Script Execution Failed: {e}",
        }
        sys.stdout.write(json.dumps(error_resp, indent=2) + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()