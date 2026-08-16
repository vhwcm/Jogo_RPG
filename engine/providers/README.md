# 🤖 Submódulo Providers (`engine/providers`)

O submódulo `engine/providers` encapsula e padroniza a comunicação com diferentes provedores de Modelos de Linguagem Grande (LLMs) e modelos de embeddings.

---

## 📂 Arquivos do Módulo

- **`base.py`**: Interface abstrata `BaseLLMProvider` definindo o contrato obrigatório para todos os provedores.
- **`factory.py`**: Implementação do padrão Factory (`LLMFactory`) para registro, listagem e instanciação dinâmica dos provedores.
- **`gemini_provider.py`**: Adaptador para a API Google Gemini (modelos `gemini-2.5-flash` e `text-embedding-004`).
- **`grok_provider.py`**: Adaptador para a API xAI Grok (modelo `grok-2-latest`).
- **`openai_provider.py`**: Adaptador para a API OpenAI (modelos `gpt-4o-mini` e `text-embedding-3-small`).
- **`ollama_provider.py`**: Adaptador para inferência local via servidor Ollama (ex: `llama3`, `mistral`).

---

## 🔌 Contrato da Interface Base (`BaseLLMProvider`)

Qualquer novo provedor implementa os seguintes métodos fundamentais:

```python
class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_turn(self, system_instruction: str, prompt: str) -> Dict[str, Any]:
        """Gera a resposta do turno estruturada em JSON."""
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Gera o vetor numérico de embeddings para recuperação no RAG."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se as chaves de API necessárias estão configuradas e ativas."""
        pass
```

---

## ⚙️ Alternando Provedores

A troca de provedor pode ser feita via arquivo `.env`, via requisição na API FastAPI ou diretamente no código via Factory:

```python
from engine.providers.factory import LLMFactory

# Obter o provedor padrão configurado no .env
provider = LLMFactory.get_default_provider()

# Obter um provedor específico
gemini = LLMFactory.get_provider("gemini")
grok = LLMFactory.get_provider("grok")
openai = LLMFactory.get_provider("openai")
ollama = LLMFactory.get_provider("ollama")
```
