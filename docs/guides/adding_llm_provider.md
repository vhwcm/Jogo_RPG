# 🔌 Guide: Adding a New LLM Provider

## Visão Geral
Este guia detalha as etapas para integrar um novo provedor de Inteligência Artificial (ex: Anthropic Claude, Mistral AI, Cohere) mantendo a conformidade com a Clean Architecture do projeto.

---

## Passo 1: Implementar a Interface `BaseLLMProvider`

Crie o arquivo `engine/providers/<nome>_provider.py`:

```python
from typing import Dict, Any, List
from engine.providers.base import BaseLLMProvider
import config

class CustomProvider(BaseLLMProvider):
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or getattr(config, "CUSTOM_API_KEY", "")
        self.model = model or getattr(config, "CUSTOM_MODEL", "custom-model-name")

    @property
    def name(self) -> str:
        return "custom"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate_text(self, prompt: str, system_instruction: str = None) -> str:
        # Chamada HTTP ou SDK da API
        ...

    def generate_json(self, prompt: str, system_instruction: str = None) -> Dict[str, Any]:
        # Parsing defensivo de JSON
        ...

    def generate_embedding(self, text: str) -> List[float]:
        # Geração de vetor ou fallback para generate_fallback_embedding(text)
        ...
```

---

## Passo 2: Registrar na Fábrica (`engine/providers/factory.py`)

No método `LLMFactory.get_provider()`:

```python
elif name == "custom":
    from engine.providers.custom_provider import CustomProvider
    primary = CustomProvider()
```

---

## Passo 3: Configurar Variáveis de Ambiente (`config.py` e `.env`)

Adicione em `config.py`:
```python
CUSTOM_API_KEY = os.getenv("CUSTOM_API_KEY", "")
CUSTOM_MODEL = os.getenv("CUSTOM_MODEL", "custom-default")
```

---

## Passo 4: Criar Testes Unitários (`tests/test_providers.py`)

Adicione testes validando que o provider responde a `generate_text`, `generate_json` e trata falhas corretamente.
