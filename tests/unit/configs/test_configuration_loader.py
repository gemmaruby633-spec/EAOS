"""Unit tests for configs/ package."""

from __future__ import annotations

from pathlib import Path

from configs.config_loader import ConfigurationLoaderEngine


def test_configuration_loader_engine(tmp_path: Path) -> None:
    """Test loading declarative environment configurations."""
    env_dir = tmp_path / "configs" / "production"
    env_dir.mkdir(parents=True, exist_ok=True)
    (env_dir / "settings.yaml").write_text("app_env: production\nport: 8000")

    pol_file = tmp_path / "configs" / "governance_policy.yaml"
    pol_file.write_text("policy_name: rbac_enforced")

    engine = ConfigurationLoaderEngine(workspace_root=tmp_path)
    config = engine.load_environment_config("production")

    assert config.environment_name == "production"
    assert config.settings_data.get("app_env") == "production"
    assert config.policy_data.get("policy_name") == "rbac_enforced"
    assert config.is_airgapped is False
