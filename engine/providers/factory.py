from typing import List, Dict, Any, Optional
from engine.providers.base import BaseLLMProvider
from engine.providers.gemini_provider import GeminiProvider
from engine.providers.grok_provider import GrokProvider
from engine.providers.openai_provider import OpenAIProvider
from engine.providers.ollama_provider import OllamaProvider
from engine.utils import generate_fallback_embedding
import config

class MockFallbackProvider(BaseLLMProvider):
    @property
    def name(self) -> str:
        return "mock_fallback"

    def is_available(self) -> bool:
        return True

    def generate_text(self, prompt: str, system_instruction: str = "", temperature: float = 0.5) -> str:
        return "Os oráculos vislumbram o destino em silêncio. (Modo Offline / Sem API Key configurada)"

    def generate_json(self, prompt: str, system_instruction: str = "", temperature: float = 0.4) -> Dict[str, Any]:
        import re
        kingdom_match = re.search(r"reino\s+['\"]?([^'\",\.]+)", prompt, re.IGNORECASE)
        ruler_match = re.search(r"Imperador(?:\(a\))?\s+['\"]?([^'\",\.]+)", prompt, re.IGNORECASE)

        kingdom_name = kingdom_match.group(1).strip() if kingdom_match else "Reino Desconhecido"
        ruler_name = ruler_match.group(1).strip() if ruler_match else "Majestade"

        if "INÍCIO DE CAMPANHA" in prompt or "Religião Oficial: Nenhuma" in prompt:
            aventura_text = (
                f"Saudações, Vossa Majestade {ruler_name}. O reino de {kingdom_name} recém-fundado ainda não possui uma fé oficial ('Nenhuma'). "
                "Como primeiro ato de vosso reinado, qual doutrina espiritual devemos adotar para guiar nosso povo?\n"
                "1. Fundar a Ordem da Luz Divina para unificar a fé\n"
                "2. Adorar os Antigos Deuses da Natureza e dos Elementos\n"
                "3. Manter o Reino laico, focando na Razão, Ciência e Filosofia"
            )
        else:
            aventura_text = f"Os escribas reais do reino de {kingdom_name} aguardam suas ordens, Majestade."

        return {
            "aventura": aventura_text,
            "opcoes": [
                "1. Fundar a Ordem da Luz Divina para unificar a fé",
                "2. Adorar os Antigos Deuses da Natureza e dos Elementos",
                "3. Manter o Reino laico, focando na Razão, Ciência e Filosofia"
            ],
            "status_reino": {
                "nome_reino": kingdom_name,
                "imperador": ruler_name,
                "dinheiro": 5000,
                "populacao": 10000,
                "religião": "Nenhuma",
                "poder_militar": 1000,
                "felicidade": "70%"
            }
        }

    def generate_embedding(self, text: str) -> List[float]:
        return generate_fallback_embedding(text)


class FallbackLLMProvider(BaseLLMProvider):
    def __init__(self, primary: BaseLLMProvider, fallbacks: List[BaseLLMProvider]):
        self.primary = primary
        self.fallbacks = fallbacks

    @property
    def name(self) -> str:
        return f"{self.primary.name}_with_fallbacks"

    def is_available(self) -> bool:
        if self.primary.is_available():
            return True
        return any(f.is_available() for f in self.fallbacks)

    def generate_text(self, prompt: str, system_instruction: str = "", temperature: float = 0.5) -> str:
        candidates = [self.primary] + self.fallbacks
        for provider in candidates:
            if provider.is_available():
                try:
                    return provider.generate_text(prompt, system_instruction, temperature)
                except Exception as e:
                    print(f"Warning: Provider '{provider.name}' failed generate_text ({e}). Trying next fallback...")
        return MockFallbackProvider().generate_text(prompt, system_instruction, temperature)

    def generate_json(self, prompt: str, system_instruction: str = "", temperature: float = 0.4) -> Dict[str, Any]:
        candidates = [self.primary] + self.fallbacks
        for provider in candidates:
            if provider.is_available():
                try:
                    return provider.generate_json(prompt, system_instruction, temperature)
                except Exception as e:
                    print(f"Warning: Provider '{provider.name}' failed generate_json ({e}). Trying next fallback...")
        return MockFallbackProvider().json.loads("{}") if hasattr(MockFallbackProvider(), 'json') else MockFallbackProvider().generate_json(prompt, system_instruction, temperature)

    def generate_embedding(self, text: str) -> List[float]:
        candidates = [self.primary] + self.fallbacks
        for provider in candidates:
            if provider.is_available():
                try:
                    return provider.generate_embedding(text)
                except Exception as e:
                    pass
        return MockFallbackProvider().generate_embedding(text)


class LLMFactory:
    @staticmethod
    def get_provider(preferred_name: Optional[str] = None) -> BaseLLMProvider:
        provider_name = (preferred_name or config.DEFAULT_PROVIDER).lower()
        
        providers_map = {
            "gemini": GeminiProvider(),
            "grok": GrokProvider(),
            "openai": OpenAIProvider(),
            "ollama": OllamaProvider(),
            "mock_fallback": MockFallbackProvider(),
        }
        
        primary = providers_map.get(provider_name, GeminiProvider())
        fallbacks = [p for name, p in providers_map.items() if name != provider_name]
        if "mock_fallback" not in [p.name for p in fallbacks] and primary.name != "mock_fallback":
            fallbacks.append(MockFallbackProvider())
        
        return FallbackLLMProvider(primary, fallbacks)
