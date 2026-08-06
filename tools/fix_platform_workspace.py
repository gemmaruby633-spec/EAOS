"""Fix UV Workspace Members and Dependencies for Platforms."""

from __future__ import annotations

from pathlib import Path


def fix_platform_workspace() -> None:
    root = Path("D:/EAOS").resolve()
    p_toml = root / "pyproject.toml"

    # 1. Ensure platforms/pyproject.toml exists
    ps_dir = root / "platforms"
    if ps_dir.exists():
        ps_toml = ps_dir / "pyproject.toml"
        if not ps_toml.exists():
            content = (
                "[project]\n"
                'name = "eaos-platform-services"\n'
                'version = "0.1.0"\n'
                'description = "EAOS Platform Services Shim"\n'
                'requires-python = ">=3.14"\n'
                "dependencies = []\n\n"
                "[build-system]\n"
                'requires = ["hatchling"]\n'
                'build-backend = "hatchling.build"\n'
            )
            ps_toml.write_text(content, encoding="utf-8")
            print("  ✔ Created platforms/pyproject.toml")

    # 2. Ensure platforms/pyproject.toml exists
    plt_dir = root / "platforms"
    if plt_dir.exists():
        plt_toml = plt_dir / "pyproject.toml"
        if not plt_toml.exists():
            content = (
                "[project]\n"
                'name = "eaos-platforms"\n'
                'version = "0.1.0"\n'
                'description = "EAOS Unified Platforms Package"\n'
                'requires-python = ">=3.14"\n'
                "dependencies = []\n\n"
                "[build-system]\n"
                'requires = ["hatchling"]\n'
                'build-backend = "hatchling.build"\n'
            )
            plt_toml.write_text(content, encoding="utf-8")
            print("  ✔ Created platforms/pyproject.toml")

    # 3. Update root pyproject.toml
    text = p_toml.read_text(encoding="utf-8")

    if '"platforms"' not in text and "workspace = { members = [" in text:
        text = text.replace(
            "workspace = { members = [",
            'workspace = { members = [\n    "platforms",',
        )

    if "eaos-platforms = { workspace = true }" not in text:
        text = text.replace(
            "[tool.uv.sources]",
            "[tool.uv.sources]\neaos-platforms = { workspace = true }",
        )

    p_toml.write_text(text, encoding="utf-8")
    print("  ✔ Updated root pyproject.toml with platforms workspace member")


if __name__ == "__main__":
    fix_platform_workspace()
