"""Unit tests for apps/ sub-application entrypoints."""

from __future__ import annotations

from apps.api.app.dto.api_response_dto import APIStandardResponseDTO


def test_api_standard_response_dto() -> None:
    """Test standard API response DTO."""
    res = APIStandardResponseDTO(message="Test OK")
    assert res.status.upper() == "SUCCESS"
    assert res.message == "Test OK"
