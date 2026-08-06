"""Abstract AI Provider Ports for Model-Agnostic LLM Integration."""

from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict, Field


class LLMRequestDTO(BaseModel):
    """Value object representing a generic LLM completion request."""

    model_config = ConfigDict(frozen=True)

    prompt: str = Field(..., description="Input prompt text")
    model_name: str | None = Field(default=None)
    temperature: float = Field(default=0.2)
    max_tokens: int = Field(default=1024)


class LLMResponseDTO(BaseModel):
    """Value object representing an LLM completion response."""

    model_config = ConfigDict(frozen=True)

    provider_name: str
    model_name: str
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0


class LLMProviderPort(ABC):
    """Abstract Port interface for all AI Model Provider Adapters."""

    @abstractmethod
    async def generate_async(self, request: LLMRequestDTO) -> LLMResponseDTO:
        """Asynchronously generates text completion from LLM provider."""
