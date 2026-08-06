"""UI Plugin Manager Adapter implementing Meta-Layer Architecture."""

from __future__ import annotations

from packages.design_system.domain.ui_capability_models import (
    CommandPaletteAction,
    PanelWidgetConfig,
    WorkspaceLayoutConfig,
)
from packages.design_system.ports.ui_plugin_port import (
    UIPluginManagerPort,
)


class UIPluginManagerAdapter(UIPluginManagerPort):
    """Adapter managing UI capability plugins, commands, and layouts."""

    def __init__(self) -> None:
        self._commands: dict[str, CommandPaletteAction] = {}
        self._register_default_commands()

    def _register_default_commands(self) -> None:
        defaults = [
            CommandPaletteAction(
                action_id="cmd-doctor",
                title="Run Enterprise Doctor",
                category="OPERATIONS",
                shortcut="Ctrl+Shift+D",
            ),
            CommandPaletteAction(
                action_id="cmd-validate",
                title="Validate Architecture Boundaries",
                category="GOVERNANCE",
                shortcut="Ctrl+Shift+V",
            ),
            CommandPaletteAction(
                action_id="cmd-benchmark",
                title="Run Swarm & RAG Benchmark",
                category="PERFORMANCE",
                shortcut="Ctrl+Shift+B",
            ),
        ]
        for cmd in defaults:
            self.register_command(cmd)

    def register_command(self, action: CommandPaletteAction) -> None:
        self._commands[action.action_id] = action

    def get_command_palette(self) -> list[CommandPaletteAction]:
        return list(self._commands.values())

    def get_persona_layout(self, persona: str) -> WorkspaceLayoutConfig:
        widgets = [
            PanelWidgetConfig(widget_id="w-chat", widget_type="CHAT"),
            PanelWidgetConfig(
                widget_id="w-diff",
                widget_type="DIFF",
                dock_position="RIGHT",
            ),
            PanelWidgetConfig(
                widget_id="w-term",
                widget_type="TERMINAL",
                dock_position="BOTTOM",
            ),
        ]
        return WorkspaceLayoutConfig(
            workspace_id=f"ws-{persona}",
            persona_role=persona,
            version="1.0.0",
            widgets=widgets,
        )
