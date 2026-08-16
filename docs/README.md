# Project Knowledge Base (AI RPG Game)

Base de conhecimento persistente do **AI RPG Game**, estruturada segundo os princípios do modelo mental do Kiro.

---

## Mapa da Base de Conhecimento

### Arquitetura (`docs/architecture/`)
- [**Visão Geral da Arquitetura**](architecture/overview.md) — Stack, componentes, limites e princípios de Clean Architecture.
- [**Backend & API Server**](architecture/backend.md) — FastAPI, orquestração de GameEngine, DTOs e endpoints.
- [**Frontend Web SPA**](architecture/frontend.md) — Design Glassmorphism, Web Audio Manager e componentes.
- [**Banco de Dados & Vector Store**](architecture/database.md) — Schema SQLite3, modo WAL, integridade e armazenamento vetorial.
- [**Infraestrutura & Configurações**](architecture/infrastructure.md) — Variáveis de ambiente, scripts de inicialização e diagnósticos.

### Dominio (`docs/domain/`)
- [**Campanhas**](domain/campaigns.md) — Ciclo de vida, isolamento e agregação de histórico.
- [**Estado do Reino & Decisões**](domain/kingdom_state.md) — Métricas de recursos, opções, impactos e humor emocional.
- [**Personagens & NPCs**](domain/characters_and_npcs.md) — Entidades, cargos, lealdade e grafos de conhecimento.
- [**Missões & Quests**](domain/quests.md) — Gestão de objetivos de estado e recompensas.
- [**Memória & RAG**](domain/memory_and_rag.md) — Arquitetura de memória em 4 camadas e busca semântica híbrida.
- [**Provedores de LLM & Fallback**](domain/providers_and_llm.md) — Integrações de IA, cadeias de redundância e contratos JSON.

### Decisoes Arquiteturais (`docs/decisions/`)
- [**ADR-001: Clean Layered Architecture**](decisions/ADR-001-clean-layered-architecture.md)
- [**ADR-002: SQLite3 & Memória Episódica RAG**](decisions/ADR-002-sqlite3-and-vector-rag-memory.md)
- [**ADR-003: Provedores Plugáveis & Cadeia de Fallback**](decisions/ADR-003-pluggable-llm-providers.md)
- [**ADR-004: Interface Web Glassmorphic & API FastAPI**](decisions/ADR-004-fastapi-and-glassmorphism-web-ui.md)
- [**ADR-005: Suíte Pytest & Diagnóstico de APIs**](decisions/ADR-005-pytest-suite-and-api-diagnostics.md)
- [**ADR-006: Observabilidade, Logs Estruturados & Padrão Visual D2**](decisions/ADR-006-observability-logs-and-d2-visual-documentation.md)

### Diagramas D2 (`docs/diagrams/`)
- [**Camadas da Arquitetura Limpa**](diagrams/architecture_layers.d2) — Visão de componentes, isolamento de camadas e conexões.
- [**Ciclo de Execução de Turnos**](diagrams/turn_execution_flow.d2) — Fluxo ponta a ponta de requisição, RAG, inferência e persistência.
- [**Fluxo de Observabilidade & Troubleshooting**](diagrams/observability_troubleshooting_flow.d2) — Instrumentação de logs e rotina de resolução orientada a evidências.

### Subsistemas (`docs/systems/`)
- [**Ciclo de Execução de Turnos**](systems/turn_execution.md) — Fluxo ponta a ponta da entrada do jogador à resposta estruturada.
- [**Sumarizador Hierárquico de Campanhas**](systems/summarizer.md) — Compressão periódica de crônicas para controle de tokens.
- [**Importação & Exportação de Savegames**](systems/import_export.md) — Portabilidade de partidas via JSON.
- [**Mecanismo de Rollback**](systems/rollback.md) — Reversão segura de estado e poda de memórias órfãs.

### Guias & Procedimentos (`docs/guides/`)
- [**Setup & Execução**](guides/setup_and_run.md) — Guia prático de instalação, configuração e inicialização.
- [**Adicionando Novos Provedores de IA**](guides/adding_llm_provider.md) — Passo a passo para estender a camada de LLMs.
- [**Guia de Testes & Qualidade**](guides/testing_guide.md) — Padrões e execução da suíte de testes com Pytest.
- [**Observabilidade, Logs & Troubleshooting**](guides/observability_and_troubleshooting.md) — Padrões de logging estruturado e catálogo de procedimentos.
- [**Guia de Padrões para Diagramas D2**](guides/d2_diagrams_guide.md) — Convenções para documentação visual com D2.
