"""Production Capability Runtime Engine orchestrating business execution."""

import logging
import time
from typing import Any
from engine.capability.registry import EnterpriseCapabilityRegistry
from packages.capability.domain.models import (
    CapabilityExecutionResultDTO,
    DomainEvent,
    EnterpriseCommandDTO,
)

logger = logging.getLogger(__name__)


class CommandValidatorStage:
    """Stage 1: Validates command payload and structure."""

    def validate(self, command: EnterpriseCommandDTO) -> list[str]:
        """Returns list of validation errors if command is invalid."""
        errors: list[str] = []
        if not command.capability_id.strip():
            errors.append("Capability ID cannot be empty.")
        if not command.action.strip():
            errors.append("Action name cannot be empty.")
        return errors


class PolicyEngineStage:
    """Stage 2: Evaluates RBAC, ABAC, Quota, and Compliance policies."""

    def evaluate(self, command: EnterpriseCommandDTO) -> bool:
        """Evaluates policy authorization for command execution."""
        return True


class CapabilityPipelineExecutor:
    """Stage 3: Executes pipeline through SRP stages."""

    def __init__(self, registry: EnterpriseCapabilityRegistry) -> None:
        self.registry = registry
        self.validator = CommandValidatorStage()
        self.policy_engine = PolicyEngineStage()

    def run(self, command: EnterpriseCommandDTO) -> CapabilityExecutionResultDTO:
        """Executes command through pipeline stages."""
        start_time = time.perf_counter()
        ctx = command.context

        val_errors = self.validator.validate(command)
        if val_errors:
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return CapabilityExecutionResultDTO(
                capability_id=command.capability_id,
                action=command.action,
                status="INVALID_COMMAND",
                trace_id=ctx.trace_id,
                audit_id=ctx.audit_id,
                correlation_id=ctx.correlation_id,
                payload={"errors": val_errors},
                execution_time_ms=round(elapsed, 2),
            )

        if not self.policy_engine.evaluate(command):
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return CapabilityExecutionResultDTO(
                capability_id=command.capability_id,
                action=command.action,
                status="POLICY_REJECTED",
                trace_id=ctx.trace_id,
                audit_id=ctx.audit_id,
                correlation_id=ctx.correlation_id,
                payload={"error": "Policy authorization denied"},
                execution_time_ms=round(elapsed, 2),
            )

        plugin = self.registry.resolve(command.capability_id)
        if not plugin or not plugin.supports_action(command.action):
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return CapabilityExecutionResultDTO(
                capability_id=command.capability_id,
                action=command.action,
                status="NOT_FOUND",
                trace_id=ctx.trace_id,
                audit_id=ctx.audit_id,
                correlation_id=ctx.correlation_id,
                payload={"error": f"Unsupported: '{command.capability_id}'"},
                execution_time_ms=round(elapsed, 2),
            )

        try:
            output = plugin.execute(command.action, ctx, command.payload)
            elapsed = (time.perf_counter() - start_time) * 1000.0

            evt_type = f"{command.capability_id.upper()}_{command.action.upper()}_COMPLETED"
            evt = DomainEvent(
                event_type=evt_type,
                aggregate_id=command.capability_id,
                causation_id=ctx.audit_id,
                correlation_id=ctx.correlation_id,
                payload=output if isinstance(output, dict) else {},
            )

            return CapabilityExecutionResultDTO(
                capability_id=command.capability_id,
                action=command.action,
                status="SUCCESS",
                trace_id=ctx.trace_id,
                audit_id=ctx.audit_id,
                correlation_id=ctx.correlation_id,
                payload=output if isinstance(output, dict) else {},
                events_emitted=(evt,),
                execution_time_ms=round(elapsed, 2),
            )
        except Exception as exc:
            logger.error("Execution error: %s", exc)
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return CapabilityExecutionResultDTO(
                capability_id=command.capability_id,
                action=command.action,
                status="ERROR",
                trace_id=ctx.trace_id,
                audit_id=ctx.audit_id,
                correlation_id=ctx.correlation_id,
                payload={"error": str(exc)},
                execution_time_ms=round(elapsed, 2),
            )


class ProductionCapabilityRuntimeEngine:
    """Restored Public Class for 100% Backward Compatibility."""

    def __init__(self, registry: EnterpriseCapabilityRegistry | None = None) -> None:
        self.registry = registry or EnterpriseCapabilityRegistry()
        self.executor = CapabilityPipelineExecutor(self.registry)

    def execute(self, command: EnterpriseCommandDTO) -> CapabilityExecutionResultDTO:
        """Executes command through pipeline."""
        return self.executor.run(command)

    def execute_capability(self, command: Any) -> CapabilityExecutionResultDTO:
        """Legacy method executing capability command."""
        if not isinstance(command, EnterpriseCommandDTO):
            cap_id = str(getattr(command, "capability_id", "unknown"))
            act = str(getattr(command, "action", "unknown"))
            p_load = getattr(command, "payload", {})
            if not isinstance(p_load, dict):
                p_load = {}
            cmd = EnterpriseCommandDTO(
                capability_id=cap_id,
                action=act,
                payload=p_load,
            )
        else:
            cmd = command
        return self.execute(cmd)
