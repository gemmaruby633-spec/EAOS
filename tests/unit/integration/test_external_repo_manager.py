"""Unit tests for External Repository Manager Adapter."""

from __future__ import annotations

from pathlib import Path

import pytest
from packages.federation.adapters.external_repo_manager_adapter import (
    ExternalRepositoryManagerAdapter,
)
from packages.federation.domain.repository_onboarding_models import (
    StackType,
)


@pytest.mark.anyio
async def test_external_repository_installation_mock(
    tmp_path: Path,
) -> None:
    """Test onboarding and stack detection for external repos."""
    adapter = ExternalRepositoryManagerAdapter(workspace_root=tmp_path)

    mock_repo = tmp_path / "runtime" / "external_repos" / "sample_tool"
    mock_repo.mkdir(parents=True, exist_ok=True)
    (mock_repo / "pyproject.toml").write_text("[project]\nname='sample'")

    report = await adapter.install_repository("sample_tool")

    assert report.success is True
    assert report.repo_name == "sample_tool"
    assert report.stack_type == StackType.PYTHON
    assert "cap-external-sample_tool" in report.capability_id

    installed = adapter.list_installed_repositories()
    assert len(installed) == 1
    assert installed[0].repo_name == "sample_tool"
