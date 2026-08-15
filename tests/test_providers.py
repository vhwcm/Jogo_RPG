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
