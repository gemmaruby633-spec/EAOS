"""Middleware registration for EAOS API Gateway."""

from fastapi import FastAPI


def register_middlewares(app: FastAPI) -> None:
    """Registers global security, tracing, and observability middlewares."""
