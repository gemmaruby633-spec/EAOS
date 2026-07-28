"""Ollama Infrastructure Adapter implementing LLMProviderPort."""

import logging
import httpx
from packages.ai_gateway.domain.models import (
    AIProviderTimeoutError,
    AIProviderUnavailableError,
    LLMRequestDTO,
    LLMResponseDTO,
)
from packages.ai_gateway.domain.ports import LLMProviderPort

logger = logging.getLogger(__name__)


class OllamaAdapter(LLMProviderPort):
    """Adapter communicating with Ollama REST API via httpx."""

    def __init__(
        self,
        endpoint: str = "http://localhost:11434",
        connect_timeout: float = 5.0,
        read_timeout: float = 120.0,
        write_timeout: float = 30.0,
        pool_timeout: float = 5.0,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.timeout_config = httpx.Timeout(
            connect=connect_timeout,
            read=read_timeout,
            write=write_timeout,
            pool=pool_timeout,
        )

    async def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        """Generates completion from Ollama REST endpoint."""
        url = f"{self.endpoint}/api/generate"
        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": False,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_config) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                content = str(data.get("response", ""))
                return LLMResponseDTO(
                    content=content,
                    provider="ollama",
                    model_used=request.model,
                    tokens_used=int(data.get("eval_count", 0)),
                )
        except httpx.TimeoutException as e:
            logger.warning("Ollama request timed out on %s: %s", url, e)
            raise AIProviderTimeoutError("Ollama request timed out") from e
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.error("Ollama connection error on %s: %s", url, e)
            raise AIProviderUnavailableError(f"Ollama error: {e}") from e

    async def health_check(self) -> bool:
        """Checks if Ollama service is responsive."""
        url = f"{self.endpoint}/api/version"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(url)
                return resp.status_code == 200
        except Exception as e:
            logger.debug("Ollama health check failed: %s", e)
            return False
