"""Unit tests for Multi-Key Round-Robin & Resilient AI Gateway."""

from platforms.ai.llm_gateway import (
    GeminiKeyRotator,
    MultiProviderResilientGateway,
)
from platforms.ai.settings import EAOSSettings


def test_gemini_key_rotator_round_robin() -> None:
    rotator = GeminiKeyRotator(keys_str="key_a, key_b, key_c")
    
    k1, idx1 = rotator.get_next_key()
    assert k1 == "key_a"
    assert idx1 == 0

    k2, idx2 = rotator.get_next_key()
    assert k2 == "key_b"
    assert idx2 == 1

    k3, idx3 = rotator.get_next_key()
    assert k3 == "key_c"
    assert idx3 == 2

    # Lần gọi thứ 4 tự động xoay lại Key #0 (key_a)
    k4, idx4 = rotator.get_next_key()
    assert k4 == "key_a"
    assert idx4 == 0


def test_multi_provider_gateway_fallback_to_ollama() -> None:
    # Trường hợp không có key Gemini/Groq hợp lệ -> Tự động rơi về Ollama Offline
    settings = EAOSSettings(
        GEMINI_API_KEYS="",
        GEMINI_API_KEY="",
        GROQ_API_KEY="",
        OPENROUTER_API_KEY="",
        OLLAMA_BASE_URL="http://localhost:11434",
        OLLAMA_MODEL="nemotron-mini",
    )
    gateway = MultiProviderResilientGateway(settings=settings)
    res = gateway.generate_text("Test prompt for EAOS Architecture")

    assert res.provider_used == "ollama_local"
    assert res.model_used == "nemotron-mini"
    assert res.fallback_triggered is True