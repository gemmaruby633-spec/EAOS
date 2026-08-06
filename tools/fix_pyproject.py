"""Repair script for pyproject.toml TOML syntax."""

from __future__ import annotations

from pathlib import Path


def fix_pyproject_toml() -> None:
    """Safely fix pytest addopts array in pyproject.toml."""
    p = Path("pyproject.toml")
    lines = p.read_text(encoding="utf-8").splitlines()

    new_lines: list[str] = []
    in_section = False
    skip_array = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[tool.pytest.ini_options]"):
            in_section = True
            new_lines.append(line)
            continue

        is_new_sec = stripped.startswith("[") and not stripped.startswith("[tool.pytest")
        if in_section and is_new_sec:
            in_section = False
            skip_array = False

        if in_section and stripped.startswith("addopts"):
            new_lines.append('addopts = ["-ra", "--strict-markers"]')
            skip_array = True
            continue

        if in_section and skip_array:
            if stripped.endswith("]"):
                skip_array = False
            continue

        new_lines.append(line)

    p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print("  ✔ Successfully repaired pyproject.toml TOML syntax!")


if __name__ == "__main__":
    fix_pyproject_toml()
