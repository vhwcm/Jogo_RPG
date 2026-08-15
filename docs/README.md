# 📚 AI RPG Game - Documentação & Registros de Decisão de Arquitetura (ADRs)

Este repositório contém a documentação completa da arquitetura do motor de jogo **AI RPG Game**, seu design em camadas, os modelos de memória RAG e a lista de **Architecture Decision Records (ADRs)**.

---

## 📂 Estrutura da Documentação

- [**Visão Geral da Arquitetura (ARCHITECTURE.md)**](ARCHITECTURE.md): Diagramas de componentes, fluxo de dados, esquema de banco de dados SQLite3 e ciclo de vida de um turno.
- [**ADR 0001: Arquitetura em Camadas Decoplada (CLI & Web)**](ADR/0001-clean-layered-architecture.md)
- [**ADR 0002: Armazenamento SQLite3 e Memória Episódica RAG**](ADR/0002-sqlite3-and-vector-rag-memory.md)
- [**ADR 0003: Provedores de LLM Plugáveis (Gemini, Grok, OpenAI, Ollama)**](ADR/0003-pluggable-llm-providers-grok-gemini-openai-ollama.md)
- [**ADR 0004: Interface Web Glassmorphic e Backend FastAPI**](ADR/0004-fastapi-and-glassmorphism-web-ui.md)
- [**ADR 0005: Estratégia de Testes Pytest e Diagnóstico de APIs**](ADR/0005-pytest-suite-and-api-diagnostics.md)
