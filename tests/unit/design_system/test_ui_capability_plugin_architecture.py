"""Unit tests for UI as a Capability & Plugin Architecture (ADR-UI-002)."""

from __future__ import annotations

from packages.design_system.adapters.ui_plugin_manager_adapter import (
    UIPluginManagerAdapter,
)
from packages.design_system.domain.ui_capability_models import (
    CommandPaletteAction,
)


def test_ui_plugin_manager_commands() -> None:
    """Test registering and retrieving Command Palette actions."""
    manager = UIPluginManagerAdapter()
    cmds = manager.get_command_palette()

    assert len(cmds) >= 3
    cmd_ids = [c.action_id for c in cmds]
    assert "cmd-doctor" in cmd_ids

    new_cmd = CommandPaletteAction(
        action_id="cmd-custom",
        title="Custom Plugin Action",
        category="CUSTOM",
    )
    manager.register_command(new_cmd)
    updated_cmds = manager.get_command_palette()
    assert len(updated_cmds) == len(cmds) + 1


def test_persona_workspace_layout_generation() -> None:
    """Test layout config generation per Persona."""
    manager = UIPluginManagerAdapter()
    layout = manager.get_persona_layout("architect")

    assert layout.persona_role == "architect"
    assert len(layout.widgets) == 3
    assert layout.version == "1.0.0"
