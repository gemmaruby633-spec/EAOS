"""Factory creating AI Provider Adapter instances from environment config."""

import os

from platform_services.ai.ollama_adapter import OllamaAdapter
from platform_services.ai.ports import LLMProviderPort


class LLMProviderFactory:
    """Factory producing configured LLM Provider Adapters."""

    @staticmethod
    def get_provider() -> LLMProviderPort:
        """Instantiates provider adapter based on EAOS_AI_PROVIDER env."""
        provider = os.getenv("EAOS_AI_PROVIDER", "ollama").lower()
        ollama_url = os.getenv("EAOS_OLLAMA_URL", "http://eaos-ollama:11434")

        if provider == "ollama":
            return OllamaAdapter(base_url=ollama_url)

        return OllamaAdapter(base_url=ollama_url)


if __name__ == "__main__":
    p = LLMProviderFactory.get_provider()
    print(f"✔ AI Provider Factory active: {p.__class__.__name__}")
