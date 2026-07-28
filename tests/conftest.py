"""Pytest global configuration and Windows file lock handler."""

import gc
import pytest
from collections.abc import Generator


@pytest.fixture(autouse=True)
def auto_cleanup_handles() -> Generator[None]:
    """Fixture disposing database connections and unlinking handles."""
    yield
    gc.collect()
