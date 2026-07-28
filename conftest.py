"""Pytest global configuration, file lock handler, and shared fixtures."""

from collections.abc import Generator
import gc
from fastapi.testclient import TestClient
import pytest

from apps.api.app.main import app


@pytest.fixture(autouse=True)
def auto_cleanup_handles() -> Generator[None]:
    """Fixture disposing database connections and unlinking handles."""
    yield
    gc.collect()


@pytest.fixture
def client() -> TestClient:
    """Provides isolated FastAPI TestClient instance for all test suites."""
    return TestClient(app)
