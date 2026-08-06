"""Unit test suite verifying Phase 1 Core Engine components."""

from __future__ import annotations

from pathlib import Path

import pytest
from packages.business_architecture.adapters.file_context_adapter import (
    FileContextAdapter,
)
from packages.integration_architecture.adapters.native_tool_adapter import (
    NativeToolCallingAdapter,
)
from packages.integration_architecture.domain.tool_models import (
    ToolExecutionRequest,
)
from packages.solution_architecture.adapters.unified_patch_adapter import (
    UnifiedPatchAdapter,
)


@pytest.mark.anyio
async def test_unified_patch_engine_with_backup(tmp_path: Path) -> None:
    """Verify atomic file backup and patch application."""
    adapter = UnifiedPatchAdapter(workspace_root=tmp_path)
    sample_file = tmp_path / "sample.py"
    sample_file.write_text("def main():\n    pass\n", encoding="utf-8")

    res = await adapter.apply_patch("sample.py", "def main():\n    return 42\n")

    assert res.success is True
    assert "main" in res.diff_summary
    assert res.backup is not None
    assert Path(res.backup.backup_path).exists()


@pytest.mark.anyio
async def test_native_tool_calling_adapter(tmp_path: Path) -> None:
    """Verify native tools execution."""
    adapter = NativeToolCallingAdapter(workspace_root=tmp_path)
    tools = adapter.list_available_tools()
    assert "read_file" in tools
    assert "run_pytest" in tools

    req = ToolExecutionRequest(tool_name="list_dir", arguments={"path": "."})
    res = await adapter.execute_tool(req)
    assert res.success is True


@pytest.mark.anyio
async def test_context_engine_injection(tmp_path: Path) -> None:
    """Verify auto-injection of Constitution and ADR context."""
    adapter = FileContextAdapter(workspace_root=tmp_path)
    const_file = tmp_path / "ARCHITECTURE_CONSTITUTION.md"
    const_file.write_text("# Constitution v3.0\nRule 1: Domain First")

    injected = await adapter.inject_context_into_prompt("Add new rule")

    assert injected.user_prompt == "Add new rule"
    assert "Constitution v3.0" in injected.formatted_prompt
