# Project Agent Instructions (AI RPG Game)

Este arquivo é a regra-mãe para qualquer agente de IA que opere neste repositório. Ele define como o projeto funciona e o fluxo rigoroso de desenvolvimento inspirado no modelo mental do Kiro.

---

## 🧠 Project Knowledge as Source of Truth

Antes de implementar qualquer alteração significativa:
1. Inspecione a documentação correspondente em `docs/` e especificações ativas em `specs/`.
2. A documentação em `docs/` é a **fonte primária da verdade** para decisões arquiteturais, modelos de domínio e convenções de código.
3. Não presuma nem deduza o "porquê" de uma decisão sem antes consultar `docs/decisions/` (ADRs).

---

## 🔄 Development Workflow (Kiro Flow)

Para desenvolvimento de features, refatorações ou correções com impacto arquitetural:

```
               ┌─────────────────────┐
               │   PROJECT KNOWLEDGE │
               └──────────┬──────────┘
                          │
           ┌──────────────┼──────────────┐
           ↓              ↓              ↓
       ARCHITECTURE     DOMAIN       DECISIONS
           │              │              │
           └──────────────┼──────────────┘
                          ↓
                      CREATE SPEC
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
        REQUIREMENTS    DESIGN       TASKS
             │            │            │
             └────────────┼────────────┘
                          ↓
                    IMPLEMENTAÇÃO
                          ↓
                    TESTES (TDD)
                          ↓
                    REVIEW & AUDIT
                          ↓
                 ATUALIZA DOCUMENTAÇÃO
```

### Etapas do Fluxo:

1. **Explore Project & Context**: Execute a skill `explore-project` para inspecionar `docs/`, modelos de domínio e ADRs relevantes.
2. **Create Spec**: Para tarefas médias ou grandes, crie uma spec em `specs/active/<feature-name>/` contendo:
   - `requirements.md` (Objetivo, Requisitos Funcionais R1..Rn, Critérios de Aceite).
   - `design.md` (Arquitetura, Componentes, Mudanças de Schema/API, Tratamento de Erros).
   - `tasks.md` (Checklist atômico de tarefas de implementação).
3. **Implement Tasks**: Execute a skill `implement-spec`, seguindo estritamente o `design.md` sem inventar padrões paralelos.
4. **Test & Validate**: Rode a suíte de testes com `pytest` garantindo 100% de passagem e aderência a TDD.
5. **Review Consistency**: Execute a skill `review-consistency` para verificar alinhamento entre Requisitos ↔ Design ↔ Código ↔ Testes.
6. **Update Knowledge**: Execute a skill `update-docs` para atualizar `docs/architecture/`, `docs/domain/`, `docs/systems/` ou registrar novos ADRs se o conhecimento do projeto tiver evoluído.
7. **Archive Spec**: Mova a spec de `specs/active/` para `specs/completed/`.

---

## ⚖️ Classificação de Escopo de Tarefas

Nem toda tarefa exige uma especificação completa em `specs/`:

| Escopo | Exemplos | Fluxo Requerido |
|---|---|---|
| **Pequena (Small)** | Correção de bug trivial, ajuste de typo, refatoração local isolada, ajuste cosmético de CSS. | Implementação direta → Testes → Atualizar doc se aplicável. |
| **Média (Medium)** | Novo endpoint REST, novo método no repositório, novo componente web isolado, novo provider de LLM. | Consultar `docs/` → Criar Spec simplificada ou tasks atômicas → Implementação → Testes → Atualizar `docs/`. |
| **Grande (Large)** | Novo subsistema (ex: combate tático, árvores de diálogo), alteração no schema SQLite, mudança no motor de RAG, refatoração estrutural. | **Obrigatório**: `explore-project` → `create-spec` (Reqs + Design + Tasks) → `implement-spec` → Testes → `review-consistency` → `update-docs`. |

---

## 🚫 Regras Críticas e Invioláveis

- **Sem Comentários no Código**: Nunca adicione comentários (`#`, `//`, `/* */`) no código a menos que expressamente solicitado pelo usuário.
- **Respeito à Arquitetura em Camadas**:
  - `engine/domain/`: Lógica de domínio pura e dataclasses. Zero dependência de FastAPI ou frameworks web.
  - `engine/db/`: Todo o acesso a banco de dados SQLite deve passar por `Repository` ou `VectorStore`. Nunca execute SQL raw fora desta camada.
  - `engine/providers/`: Provedores de IA desacoplados implementando `BaseLLMProvider` e resolvidos via `LLMFactory`.
  - `server/`: Camada HTTP FastAPI com DTOs Pydantic. Zero regras de negócio em `server/app.py`.
- **Configuração Centralizada**: Todas as variáveis e segredos devem ser lidos de `config.py`. Nunca leia `.env` ou `os.environ` diretamente nos módulos internos.
- **Sincronia Estrita de Documentação**: Se o comportamento do código mudar, a documentação em `docs/` deve ser atualizada no mesmo commit/etapa.
