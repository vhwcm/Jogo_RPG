# 🤖 Domain: Pluggable LLM Providers & Fallback

## Purpose
Prover uma camada de inteligência artificial agnóstica a fornecedores (Google, OpenAI, xAI, Ollama Local), com tolerância a falhas através de cadeia de fallback automático.

---

## Contrato de Provedores (`engine/providers/base.py`)

Todos os provedores implementam a classe abstrata `BaseLLMProvider`:

```python
class BaseLLMProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    def generate_text(self, prompt: str, system_instruction: str = None) -> str: ...

    @abstractmethod
    def generate_json(self, prompt: str, system_instruction: str = None) -> Dict[str, Any]: ...

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]: ...
```

---

## Cadeia de Fallback (`FallbackLLMProvider`)

Ao solicitar um provedor via `LLMFactory.get_provider("gemini")`, a fábrica instancia um `FallbackLLMProvider` envolvendo o provedor primário e todos os demais provedores disponíveis como redundância:

```
[Requisição de Turno]
          │
          ▼
   [GeminiProvider] ─── (Falha de quota ou rede) ───┐
          │ (Sucesso)                               │
          │                                         ▼
          │                                  [GrokProvider] ─── (Falha) ───┐
          │                                         │                      │
          │                                         ▼                      ▼
          │                                  [OpenAIProvider]       [OllamaProvider]
          │                                         │                      │
          │                                         └──────────┬───────────┘
          │                                                    ▼
          └───────────────────────────► [MockFallbackProvider (Último recurso)]
```

---

## Contrato do Esquema JSON de Resposta

O Game Master deve obrigatoriamente retornar a resposta estruturada:

```json
{
  "aventura": "Texto narrativo formal em português...",
  "clima": "aventura | calmo | frenetico | harmonia | desenvolvimento | desespero",
  "opcoes": [
    {
      "texto": "1. Opção recomendada...",
      "impacto": { "dinheiro": -500, "poder_militar": 200 }
    }
  ],
  "status_reino": {
    "nome_reino": "string",
    "imperador": "string",
    "dinheiro": 5000,
    "populacao": 10000,
    "religião": "string",
    "poder_militar": 1000,
    "felicidade": "75%"
  }
}
```

---

## Related Code
- `engine/providers/base.py`: Classe base abstrata.
- `engine/providers/factory.py`: `LLMFactory` e `FallbackLLMProvider`.
- `engine/providers/gemini_provider.py`: Google Gemini SDK.
- `engine/providers/grok_provider.py`: xAI Grok REST.
- `engine/providers/openai_provider.py`: OpenAI REST.
- `engine/providers/ollama_provider.py`: Ollama Local API.
