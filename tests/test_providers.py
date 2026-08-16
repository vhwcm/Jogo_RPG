import pytest
from engine.providers.factory import LLMFactory, MockFallbackProvider, FallbackLLMProvider
from engine.providers.grok_provider import GrokProvider

def test_mock_fallback_provider():
    provider = MockFallbackProvider()
    assert provider.name == "mock_fallback"
    assert provider.is_available() is True
    
    text = provider.generate_text("Olá")
    assert "oráculos" in text.lower() or "offline" in text.lower()
    
    json_resp = provider.generate_json("Olá")
    assert "aventura" in json_resp
    assert "status_reino" in json_resp

    emb = provider.generate_embedding("teste")
    assert len(emb) == 128

def test_grok_provider_unconfigured():
    grok = GrokProvider(api_key="")
    assert grok.name == "grok"
    assert grok.is_available() is False

def test_llm_factory_fallback():
    provider = LLMFactory.get_provider("grok")
    assert provider.is_available() is True
    res = provider.generate_json("Test prompt")
    assert isinstance(res, dict)

def test_gemini_provider_cache():
    from engine.providers.gemini_provider import GeminiProvider
    p = GeminiProvider(api_key="")
    emb1 = p.generate_embedding("texto repetido")
    emb2 = p.generate_embedding("texto repetido")
    assert emb1 == emb2
    assert "texto repetido" in p._embedding_cache

def test_openai_provider_cache():
    from engine.providers.openai_provider import OpenAIProvider
    p = OpenAIProvider(api_key="")
    emb1 = p.generate_embedding("texto repetido openai")
    emb2 = p.generate_embedding("texto repetido openai")
    assert emb1 == emb2
    assert "texto repetido openai" in p._embedding_cache
