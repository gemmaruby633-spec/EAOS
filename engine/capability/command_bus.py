"""Enterprise Command Bus routing commands to Capability Pipeline."""

import logging

from packages.capability.domain.models import (
    CapabilityExecutionResultDTO,
    EnterpriseCommandDTO,
)

from engine.capability.pipeline import CapabilityPipelineExecutor

logger = logging.getLogger(__name__)


class EnterpriseCommandBus:
    """Command Bus routing commands from REST/CLI/Agents to Runtime."""

    def __init__(self, pipeline: CapabilityPipelineExecutor) -> None:
        self.pipeline = pipeline

    def dispatch(self, command: EnterpriseCommandDTO) -> CapabilityExecutionResultDTO:
        """Dispatches command to Capability Runtime Pipeline."""
        logger.info("Dispatching command for capability: %s", command.capability_id)
        return self.pipeline.run(command)
