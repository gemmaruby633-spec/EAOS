"""Unit tests for extensions/ package."""

from __future__ import annotations

from extensions.extension_registry import EAOSExtensionsEngine
from extensions.plugins.plugin_manager import (
    DynamicPluginManager,
    ExtensionPluginDTO,
)


def test_dynamic_plugin_manager() -> None:
    """Test registering and listing active plugins."""
    manager = DynamicPluginManager()
    plugins = manager.list_active_plugins()

    assert len(plugins) >= 1
    assert plugins[0].plugin_id == "plugin-devsecops-checker"

    new_p = ExtensionPluginDTO(
        plugin_id="plugin-custom-crm",
        title="Custom CRM Integration Plugin",
    )
    manager.register_plugin(new_p)

    updated = manager.list_active_plugins()
    assert len(updated) == len(plugins) + 1


def test_extensions_engine_summary() -> None:
    """Test master extensions engine summary generation."""
    engine = EAOSExtensionsEngine()
    summary = engine.get_extensions_summary()

    assert summary.total_plugins >= 1
    assert summary.plugins[0].is_enabled is True
