"""Lifespan context manager for FastAPI application startup/shutdown."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Handles application startup and shutdown events."""
    # Startup hooks
    yield
    # Shutdown hooks
