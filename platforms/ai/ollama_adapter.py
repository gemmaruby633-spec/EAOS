"""Async Ollama Provider Adapter using REST API and explicit error handling."""

import time
from typing import Any

import httpx

from platforms.ai.ports import (
    LLMProviderPort,
    LLMRequestDTO,
    LLMResponseDTO,
)


class OllamaAdapterError(Exception):
    """Base exception for Ollama provider errors."""


class OllamaModelNotFoundError(OllamaAdapterError):
    """Raised when target model is not pulled in Ollama."""


class OllamaAdapter(LLMProviderPort):
    """Async Hexagonal Adapter connecting EAOS to Ollama via REST."""

    def __init__(
        self,
        base_url: str = "http://eaos-ollama:11434",
        default_model: str = "llama3",
        timeout_sec: float = 120.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self.timeout_sec = timeout_sec

    async def generate_async(self, request: LLMRequestDTO) -> LLMResponseDTO:
        """Asynchronously generates text completion via Ollama REST API."""
        target_model = request.model_name or self.default_model
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": target_model,
            "prompt": request.prompt,
            "stream": False,
        }

        start_time = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
                resp = await client.post(endpoint, json=payload)

                if resp.status_code == 404:
                    raise OllamaModelNotFoundError(f"Model '{target_model}' not found in Ollama.")

                resp.raise_for_status()
                data: dict[str, Any] = resp.json()
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0

                return LLMResponseDTO(
                    provider_name="Ollama",
                    model_name=str(data.get("model", target_model)),
                    content=str(data.get("response", "")),
                    prompt_tokens=int(data.get("prompt_eval_count", 0)),
                    completion_tokens=int(data.get("eval_count", 0)),
                    latency_ms=round(elapsed_ms, 2),
                )
        except httpx.ConnectError as e:
            raise OllamaAdapterError(f"Connection failed to Ollama at {self.base_url}: {e}") from e
        except httpx.TimeoutException as e:
            raise OllamaAdapterError(f"Timeout waiting for Ollama response: {e}") from e
