"""FastAPI Router exposing Enterprise Command Bus & Runtime API."""

from fastapi import APIRouter
from engine.capability.command_bus import EnterpriseCommandBus
from engine.capability.pipeline import CapabilityPipelineExecutor
from engine.capability.registry import EnterpriseCapabilityRegistry
from packages.capability.domain.models import (
    CapabilityExecutionResultDTO,
    EnterpriseCommandDTO,
)
from packages.marketing.infrastructure.plugin import (
    MarketingCapabilityPlugin,
)

# Composition Root Assembly
_registry = EnterpriseCapabilityRegistry()
_registry.register(MarketingCapabilityPlugin())
_pipeline = CapabilityPipelineExecutor(_registry)
_command_bus = EnterpriseCommandBus(_pipeline)

router = APIRouter(prefix="/v1/capability", tags=["Capability Runtime"])


@router.post("/execute", response_model=CapabilityExecutionResultDTO)
async def execute_capability_command(
    command: EnterpriseCommandDTO,
) -> CapabilityExecutionResultDTO:
    """Dispatches a command through Enterprise Command Bus."""
    return _command_bus.dispatch(command)
