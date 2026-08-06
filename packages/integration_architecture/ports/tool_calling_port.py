"""Native Tool Calling Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.integration_architecture.domain.tool_models import (
    ToolExecutionRequest,
    ToolExecutionResult,
)


@runtime_checkable
class NativeToolCallingPort(Protocol):
    """Port protocol for executing native workspace tools."""

    async def execute_tool(self, request: ToolExecutionRequest) -> ToolExecutionResult: ...

    def list_available_tools(self) -> list[str]: ...
