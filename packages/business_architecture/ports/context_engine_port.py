"""Context Engine Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.business_architecture.domain.context_models import (
    InjectedPromptContext,
    SystemContextPayload,
)


@runtime_checkable
class ContextEnginePort(Protocol):
    """Port protocol for auto-injecting Enterprise Context."""

    async def build_system_context(self) -> SystemContextPayload: ...

    async def inject_context_into_prompt(self, user_prompt: str) -> InjectedPromptContext: ...
