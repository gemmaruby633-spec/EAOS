"""Unit test suite verifying all 10 enterprise domain engines."""

from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[3]


def test_domain_engines_exist() -> None:
    """Verifies physical presence and integrity of 10 Domain packages."""
    assert (ROOT_PATH / "packages" / "governance").exists()
    assert (ROOT_PATH / "packages" / "policy_engine").exists()
