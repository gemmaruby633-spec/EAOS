"""Health check and root status router."""

from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from tools.dashboard.control_room import ControlRoomDashboard

router = APIRouter(tags=["Health"])
ROOT_PATH = Path(__file__).resolve().parents[4]


class HealthResponse(BaseModel):
    status: str
    version: str
    governance: str


_HEALTH_RESPONSE_CACHE = HealthResponse(
    status="healthy",
    version="0.1.0",
    governance="ARCHITECTURE_CONSTITUTION.md v2.0",
)


@router.get("/")
async def root_system_status() -> dict[str, str]:
    return {
        "system": "Enterprise Architecture Operating System (EAOS)",
        "status": "ACTIVE",
        "version": "0.1.0",
        "governance": "ARCHITECTURE_CONSTITUTION.md v3.0",
    }


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return _HEALTH_RESPONSE_CACHE


@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard() -> HTMLResponse:
    dashboard = ControlRoomDashboard(ROOT_PATH)
    return HTMLResponse(content=dashboard.render_html())
