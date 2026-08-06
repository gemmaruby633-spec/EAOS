"""AI model provider types."""

from __future__ import annotations

from enum import StrEnum


class AIProviderType(StrEnum):
    """AI Provider Types."""

    GROQ = "GROQ"
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"
