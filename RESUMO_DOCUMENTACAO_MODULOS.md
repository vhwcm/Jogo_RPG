# 📋 Resumo da Documentação dos Módulos do Sistema

Criamos arquivos de documentação `README.md` detalhados em todas as principais pastas e submódulos do repositório, mapeando a arquitetura, responsabilidades, contratos de interfaces, fluxo de dados e formas de execução.

---

## 🗂️ Arquivos de Documentação Criados

| Módulo / Pasta | Arquivo Criado | Finalidade e Conteúdo |
|---|---|---|
| **`engine/`** | [`engine/README.md`](file:///home/exati/AI_RPG_GAME/engine/README.md) | Visão geral do motor do jogo, Clean Architecture, orquestração de turnos e integração de subsistemas. |
| **`engine/db/`** | [`engine/db/README.md`](file:///home/exati/AI_RPG_GAME/engine/db/README.md) | Camada de persistência relacional SQLite, DDL do schema, padrão Repository (CRUD) e Vector Store RAG com similaridade de cosseno. |
| **`engine/domain/`** | [`engine/domain/README.md`](file:///home/exati/AI_RPG_GAME/engine/domain/README.md) | Modelos de domínio `@dataclass` (`Item`, `Task`, `ImperioAliado`, `GameAction`, etc.) e máquina de estados (`GameEngine`). |
| **`engine/memory/`** | [`engine/memory/README.md`](file:///home/exati/AI_RPG_GAME/engine/memory/README.md) | Arquitetura de memória em 4 camadas, montagem dinâmica de contexto (`ContextBuilder`), algoritmo de relevância (`importance.py`) e compressão de capítulos (`summarizer.py`). |
| **`engine/providers/`** | [`engine/providers/README.md`](file:///home/exati/AI_RPG_GAME/engine/providers/README.md) | Camada de abstração de LLMs, interface base `BaseLLMProvider`, padrão Factory e adaptadores para Google Gemini, xAI Grok, OpenAI e Ollama. |
| **`server/`** | [`server/README.md`](file:///home/exati/AI_RPG_GAME/server/README.md) | Backend API REST em FastAPI, schemas Pydantic (DTOs), catálogo completo de endpoints e instruções de execução. |
| **`web/`** | [`web/README.md`](file:///home/exati/AI_RPG_GAME/web/README.md) | Interface SPA moderna com HTML5 semântico, Vanilla JS modular, Glassmorphism CSS, drawers de gerenciamento de patrimônio/diplomacia e trilha sonora adaptativa por clima narrativo. |
| **`tests/`** | [`tests/README.md`](file:///home/exati/AI_RPG_GAME/tests/README.md) | Cobertura da suíte de testes com `pytest`, descrevendo escopo de testes unitários e de integração. |
| **`data/`** | [`data/README.md`](file:///home/exati/AI_RPG_GAME/data/README.md) | Armazenamento persistente local SQLite (`rpg_game.db`), operação em modo WAL e boas práticas de backup. |
| **`terminal_rpg/`** | [`terminal_rpg/README.md`](file:///home/exati/AI_RPG_GAME/terminal_rpg/README.md) | Documentação do protótipo independente legado em modo texto para terminal. |
| **`ui_rpg/`** | [`ui_rpg/README.md`](file:///home/exati/AI_RPG_GAME/ui_rpg/README.md) | Documentação da versão desktop legada desenvolvida em Pygame e Pygame GUI, com trilha sonora e artes gráficas. |
