# 🏛️ Resumo: Implementação do Modelo Mental e Workflow Kiro

Este documento sintetiza a arquitetura de conhecimento persistente, diretrizes e workflow inspirados no **Kiro** integrados ao **AI RPG Game**.

---

## 🎯 Objetivo Alcançado
Transformar o repositório em uma base de conhecimento auto-sustentável e estruturada, onde o agente de IA consulta a documentação como fonte primária da verdade, separa planejamento de implementação através de especificações formais (`specs/`), e mantém a base sincronizada a cada evolução do código.

---

## 📂 Nova Estrutura de Conhecimento Criada

```
AI_RPG_GAME/
├── AGENTS.md                                # Manual-mestre de instruções do agente
│
├── .agent/
│   ├── rules/
│   │   ├── project.md                       # Padrões de código, tipagem, sem comentários
│   │   ├── documentation.md                 # Regras e gatilhos de sincronização de docs
│   │   ├── architecture.md                  # Limites e fronteiras invioláveis (Clean Architecture)
│   │   └── development.md                   # Classificação de tarefas (Small / Medium / Large)
│   │
│   └── skills/
│       ├── explore-project/SKILL.md         # Mapeamento do projeto antes da codificação
│       ├── create-spec/SKILL.md             # Concepção de requisitos, design e tasks
│       ├── implement-spec/SKILL.md          # Execução estrita do plano sem desvios
│       ├── update-docs/SKILL.md             # Sincronização pós-implementação
│       └── review-consistency/SKILL.md      # Auditoria cruzada de consistência
│
├── docs/
│   ├── README.md                            # Índice geral da base de conhecimento
│   ├── architecture/
│   │   ├── overview.md                      # Visão macro, stack e Clean Architecture
│   │   ├── backend.md                       # FastAPI, DTOs e orquestração da GameEngine
│   │   ├── frontend.md                      # Web SPA, Glassmorphism e áudio dinâmico
│   │   ├── database.md                      # SQLite3, modo WAL e tabelas relacionais
│   │   └── infrastructure.md                # config.py, variáveis de ambiente e diagnósticos
│   │
│   ├── domain/
│   │   ├── campaigns.md                     # Ciclo de vida e isolamento de campanhas
│   │   ├── kingdom_state.md                 # Recursos do reino, decisões e clima
│   │   ├── characters_and_npcs.md           # Modelagem de NPCs e conhecimento
│   │   ├── quests.md                        # Gestão de missões e objetivos
│   │   ├── memory_and_rag.md                # 4 camadas de memória e busca vetorial
│   │   └── providers_and_llm.md             # Provedores desacoplados e fallback
│   │
│   ├── decisions/
│   │   ├── ADR-001-clean-layered-architecture.md
│   │   ├── ADR-002-sqlite3-and-vector-rag-memory.md
│   │   ├── ADR-003-pluggable-llm-providers.md
│   │   ├── ADR-004-fastapi-and-glassmorphism-web-ui.md
│   │   └── ADR-005-pytest-suite-and-api-diagnostics.md
│   │
│   ├── systems/
│   │   ├── turn_execution.md                # Ciclo detalhado de um turno
│   │   ├── summarizer.md                    # Compressão de capítulos por IA
│   │   ├── import_export.md                 # Portabilidade de savegame em JSON
│   │   └── rollback.md                      # Reversão determinística de turnos
│   │
│   └── guides/
│       ├── setup_and_run.md                 # Guia de instalação e execução
│       ├── adding_llm_provider.md           # Como adicionar novos provedores de IA
│       └── testing_guide.md                 # Execução e padrões de testes Pytest
│
└── specs/
    ├── README.md                            # Manual do sistema de especificações
    ├── template/
    │   ├── requirements.md                  # Modelo de requisitos (R1..Rn, Critérios)
    │   ├── design.md                        # Modelo de design técnico e arquitetura
    │   └── tasks.md                         # Modelo de checklist atômico
    ├── active/                              # Especificações ativas em desenvolvimento
    └── completed/                           # Especificações concluídas e arquivadas
```

---

## 🔄 Fluxo de Trabalho Integrado

```
               [Solicitação do Usuário]
                          │
                          ▼
            [1. Avaliação de Escopo]
         ┌────────────────┴────────────────┐
         │                                 │
   (Small Task)                    (Medium / Large)
         │                                 │
         │                                 ▼
         │                    [Skill: explore-project]
         │                                 │
         │                                 ▼
         │                      [Skill: create-spec]
         │                    (requirements/design/tasks)
         │                                 │
         │                                 ▼
         └───────────────────► [Skill: implement-spec]
                                           │
                                           ▼
                                 [Testes com Pytest]
                                           │
                                           ▼
                             [Skill: review-consistency]
                                           │
                                           ▼
                                 [Skill: update-docs]
                                 (Atualiza docs/ e ADRs)
                                           │
                                           ▼
                                  [Entrega Concluída]
```
