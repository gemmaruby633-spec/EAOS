"""EAOS Enterprise API Gateway Web Entrypoint."""

from pathlib import Path
import sys

# Ensure root workspace D:\EAOS is in sys.path
ROOT_DIR = str(Path(__file__).resolve().parents[3])
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI  # noqa: E402

from apps.api.app.exception_handlers import register_exception_handlers  # noqa: E402
from apps.api.app.lifespan import lifespan  # noqa: E402
from apps.api.app.middleware import register_middlewares  # noqa: E402
from apps.api.app.routers.agents import router as agents_router  # noqa: E402
from apps.api.app.routers.autonomous import router as autonomous_router  # noqa: E402
from apps.api.app.routers.events_chaos import router as events_chaos_router  # noqa: E402
from apps.api.app.routers.federation import router as federation_router  # noqa: E402
from apps.api.app.routers.governance import router as governance_router  # noqa: E402
from apps.api.app.routers.health import router as health_router  # noqa: E402
from apps.api.app.routers.memory_knowledge import router as memory_knowledge_router  # noqa: E402
from apps.api.app.routers.metrics import router as metrics_router  # noqa: E402
from apps.api.app.routers.security import router as security_router  # noqa: E402
from apps.api.app.routers.telemetry_performance import router as telemetry_performance_router  # noqa: E402
from apps.api.app.routers.tenancy import router as tenancy_router  # noqa: E402
from apps.api.bootstrap.container import policy_evaluator  # noqa: E402

app = FastAPI(
    title="EAOS API Gateway",
    version="0.1.0",
    description="Enterprise Architecture Operating System (EAOS) v3.0",
    lifespan=lifespan,
)

register_middlewares(app)
register_exception_handlers(app)

# Include Modular Capability Routers
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(governance_router)
app.include_router(agents_router)
app.include_router(security_router)
app.include_router(federation_router)
app.include_router(autonomous_router)
app.include_router(memory_knowledge_router)
app.include_router(tenancy_router)
app.include_router(telemetry_performance_router)
app.include_router(events_chaos_router)

__all__ = ["app", "policy_evaluator"]
