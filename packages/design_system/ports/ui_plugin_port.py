"""UI Plugin Manager Port Protocol (ADR-UI-002)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.design_system.domain.ui_capability_models import (
    CommandPaletteAction,
    WorkspaceLayoutConfig,
)


@runtime_checkable
class UIPluginManagerPort(Protocol):
    """Port protocol for managing UI plugins, layouts, and commands."""

    def register_command(self, action: CommandPaletteAction) -> None: ...

    def get_command_palette(self) -> list[CommandPaletteAction]: ...

    def get_persona_layout(self, persona: str) -> WorkspaceLayoutConfig: ...
