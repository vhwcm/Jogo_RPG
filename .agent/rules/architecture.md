# Inviolable Architectural Boundaries

## 1. Clean Layered Architecture
O sistema é estritamente desacoplado nas seguintes camadas:

```
[Presentation Layer] -> Web SPA (Vanilla JS / CSS) / CLI (Rich)
        ↓ (HTTP REST DTOs)
[Interface / API Layer] -> server/ (FastAPI, Pydantic DTOs)
        ↓ (Calls GameEngine)
[Domain & Orchestration] -> engine/domain/ (GameEngine, dataclasses)
        ↓
[Memory & RAG Layer] -> engine/memory/ (ContextBuilder, Importance, Summarizer)
        ↓
[Persistence & Vector] -> engine/db/ (Repository, VectorStore, SQLite3)
        ↓
[External Providers] -> engine/providers/ (LLMFactory, BaseLLMProvider implementations)
```

## 2. Boundary Rules
- **Sem Regras de Negócio na API**: `server/app.py` apenas recebe requisições HTTP, valida DTOs Pydantic e delega a execução para métodos de `GameEngine`.
- **Isolamento de Persistência**: Nenhuma instrução SQL direta deve existir fora de `engine/db/repository.py` ou `engine/db/vector_store.py`.
- **Desacoplamento de LLM**: A `GameEngine` e o `ContextBuilder` interagem com o LLM estritamente através da interface `BaseLLMProvider`. O acesso a instâncias de provedores é sempre orquestrado via `LLMFactory.get_provider()`.
- **Integridade Relacional**: O SQLite3 opera sempre com `PRAGMA foreign_keys = ON` e journal mode `WAL`. `ON DELETE CASCADE` deve ser garantido para todas as tabelas filhas de `campaigns`.
- **Configuração Centralizada**: `config.py` é o único ponto de leitura de variáveis de ambiente. Nenhum outro arquivo deve importar `dotenv` ou ler `os.environ` diretamente.
