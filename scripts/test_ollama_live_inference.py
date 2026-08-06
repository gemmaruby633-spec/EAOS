"""Live integration test script invoking Ollama LLM via EAOS AI Adapter."""

import asyncio
import sys
from pathlib import Path

# Bootstrap root workspace path into sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from platforms.ai.ollama_adapter import (  # noqa: E402
    OllamaAdapter,
)
from platforms.ai.ports import LLMRequestDTO  # noqa: E402


async def main() -> None:
    """Executes live async text generation using pulled llama3 model."""
    adapter = OllamaAdapter(
        base_url="http://localhost:11434",
        default_model="llama3",
        timeout_sec=600,
    )
    req = LLMRequestDTO(
        prompt="Generates a 1-sentence strategic summary for EAOS.",
        model_name="llama3",
        temperature=0.2,
    )
    print("Sending prompt to local Ollama container (timeout=120s)...")
    res = await adapter.generate_async(req)
    print(f"\n✔ Model Response: {res.content}")
    print(f"✔ Prompt Tokens: {res.prompt_tokens}")
    print(f"✔ Completion Tokens: {res.completion_tokens}")
    print(f"✔ Latency: {res.latency_ms} ms")


if __name__ == "__main__":
    asyncio.run(main())
