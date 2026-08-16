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
               │ (Docs + D2 Diagrams)│
               └──────────┬──────────┘
                          │
           ┌──────────────┼──────────────┐
           ↓              ↓              ↓
       ARCHITECTURE     DOMAIN       DECISIONS
           │              │              │
           └──────────────┼──────────────┘
                          ↓
                      CREATE SPEC
              (Reqs + Design + D2 + Logs)
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
        REQUIREMENTS    DESIGN       TASKS
             │            │            │
             └────────────┼────────────┘
                          ↓
                    IMPLEMENTAÇÃO
              (Code + Structured Logs)
                          ↓
                    TESTES (TDD)
                          ↓
                    REVIEW & AUDIT
              (Code + Docs + D2 + Logs)
                          ↓
                 ATUALIZA DOCUMENTAÇÃO
               (Docs + D2 + ADRs + Guides)
```

### Etapas do Fluxo:

1. **Explore Project & Context**: Execute a skill `explore-project` para inspecionar `docs/`, diagramas D2 existentes, modelos de domínio e ADRs relevantes.
2. **Create Spec**: Para tarefas médias ou grandes, crie uma spec em `specs/active/<feature-name>/` contendo:
   - `requirements.md` (Objetivo, Requisitos Funcionais R1..Rn, Critérios de Aceite).
   - `design.md` (Arquitetura, Componentes, Diagramas D2 de fluxo/interação, Mudanças de Schema/API, Pontos de Observabilidade/Logs, Tratamento de Erros).
   - `tasks.md` (Checklist atômico de tarefas de implementação).
3. **Implement Tasks**: Execute a skill `implement-spec`, seguindo estritamente o `design.md` sem inventar padrões paralelos, instrumentando logs estruturados nos pontos-chave.
4. **Test & Validate**: Rode a suíte de testes com `pytest` garantindo 100% de passagem e aderência a TDD.
5. **Review Consistency**: Execute a skill `review-consistency` para verificar alinhamento entre Requisitos ↔ Design ↔ Código ↔ Testes ↔ Diagramas D2 ↔ Logs Estruturados.
6. **Update Knowledge**: Execute a skill `update-docs` para atualizar `docs/architecture/`, `docs/domain/`, `docs/systems/`, diagramas D2 afetados, procedimentos de troubleshooting ou registrar novos ADRs se o conhecimento do projeto tiver evoluído.
7. **Archive Spec**: Mova a spec de `specs/active/` para `specs/completed/`.

---

## 📊 Preocupações Transversais Obrigatórias

### 1. Observabilidade e Logs Estruturados
- **Instrumentação Obrigatória**: Toda funcionalidade relevante deve possuir logs estruturados nos seus pontos cruciais de execução (início de operações, tomadas de decisão, transições de estado, chamadas externas/LLM, erros e exceções).
- **Contexto Suficiente**: Os logs devem incluir dados contextuais (ex: `campaign_id`, `turn_number`, `action_type`, `provider`, `duration_ms`, `error_type`) que permitam reconstruir integralmente o que aconteceu na execução.
- **Níveis Adequados de Log**:
  - `DEBUG`: Detalhes de baixo nível, payload sanitizado, timings finos.
  - `INFO`: Marcos de ciclo de vida (início de turno, transição de estado, salvamento de partida).
  - `WARNING`: Degradações toleradas, fallbacks acionados (ex: fallback de provedor LLM), comportamentos anômalos recuperáveis.
  - `ERROR`: Falhas em operações que impediram o fluxo normal, com stack trace e contexto.
  - `CRITICAL`: Inconsistências severas de integridade referencial ou falha irrecuperável do subsistema.
- **Segurança e Privacidade (Zero Secrets)**: Informações sensíveis, senhas, chaves de API (`GEMINI_API_KEY`, `GROQ_API_KEY`, etc.) e tokens NUNCA devem ser logados.
- **Troubleshooting Baseado em Evidências**: Durante diagnósticos e investigações de problemas, o agente DEVE consultar e analisar os logs em vez de depender apenas de suposições baseadas no código.
- **Procedimentos Reutilizáveis de Troubleshooting**: Procedimentos recorrentes de diagnóstico e resolução de problemas devem ser documentados em `docs/guides/observability_and_troubleshooting.md` para consulta e reaproveitamento por agentes futuros.

### 2. Documentação Visual com D2
- **Padrão D2**: D2 é a linguagem padrão do projeto para diagramação de arquitetura, fluxo de dados, interações entre componentes e processos de negócio.
- **Gatilhos de Criação/Atualização Visual**: Sempre que uma funcionalidade criar ou alterar significativamente:
  - um fluxo de dados;
  - uma interação entre componentes;
  - um fluxo de negócio;
  - uma integração externa (LLMs, APIs, banco de dados);
  - um processo assíncrono ou ciclo de vida (turnos, sumarização, rollback);
  - uma decisão de design ou arquitetura;
  - um fluxo de autenticação/autorização;
  - um tratamento de erro relevante;
  - ou qualquer comportamento cuja compreensão visual seja vantajosa;
  o agente DEVE criar ou atualizar o diagrama D2 correspondente.
- **Localização e Referência**: Os diagramas D2 devem ser armazenados junto da documentação apropriada em `docs/diagrams/` (ou subdiretórios de `docs/` e `specs/`) e referenciados diretamente nos arquivos Markdown, Specs e ADRs pertinentes.
- **Objetivo da Documentação Visual**: Permitir que qualquer desenvolvedor ou agente compreenda o que foi construído, a relação entre componentes, o fluxo de dados, as decisões tomadas e o contexto do subsistema sem a necessidade de ler o código-fonte para deduzir essas informações.
- **Sincronização Contínua**: Quando o código ou a arquitetura mudar, o agente deve obrigatoriamente verificar quais diagramas D2 foram impactados e atualizá-los.

---

## ⚖️ Classificação de Escopo de Tarefas

Nem toda tarefa exige uma especificação completa em `specs/`:

| Escopo | Exemplos | Fluxo Requerido |
|---|---|---|
| **Pequena (Small)** | Correção de bug trivial, ajuste de typo, refatoração local isolada, ajuste cosmético de CSS. | Implementação direta → Testes → Atualizar doc/logs se aplicável. |
| **Média (Medium)** | Novo endpoint REST, novo método no repositório, novo componente web isolado, novo provider de LLM. | Consultar `docs/` e D2 → Criar Spec simplificada ou tasks atômicas com logs e diagramas D2 → Implementação → Testes → Atualizar `docs/` e D2. |
| **Grande (Large)** | Novo subsistema (ex: combate tático, árvores de diálogo), alteração no schema SQLite, mudança no motor de RAG, refatoração estrutural. | **Obrigatório**: `explore-project` (Docs + D2) → `create-spec` (Reqs + Design + D2 + Logs + Tasks) → `implement-spec` → Testes → `review-consistency` → `update-docs` (Docs + D2 + ADRs). |

---

## 🚫 Regras Críticas e Invioláveis

- **Sem Comentários no Código**: Nunca adicione comentários (`#`, `//`, `/* */`) no código a menos que expressamente solicitado pelo usuário.
- **Respeito à Arquitetura em Camadas**:
  - `engine/domain/`: Lógica de domínio pura e dataclasses. Zero dependência de FastAPI ou frameworks web.
  - `engine/db/`: Todo o acesso a banco de dados SQLite deve passar por `Repository` ou `VectorStore`. Nunca execute SQL raw fora desta camada.
  - `engine/providers/`: Provedores de IA desacoplados implementando `BaseLLMProvider` e resolvidos via `LLMFactory`.
  - `server/`: Camada HTTP FastAPI com DTOs Pydantic. Zero regras de negócio em `server/app.py`.
- **Configuração Centralizada**: Todas as variáveis e segredos devem ser lidos de `config.py`. Nunca leia `.env` ou `os.environ` diretamente nos módulos internos.
- **Observabilidade Estruturada Ativa**: As camadas do sistema devem emitir logs estruturados com contexto e níveis adequados, sem registro de segredos.
- **Sincronia Estrita de Documentação e Diagramas D2**: Se o comportamento do código ou arquitetura mudar, a documentação em `docs/` e os diagramas D2 correspondentes devem ser atualizados no mesmo commit/etapa.
- **Commit Descritivo e Push Obrigatório**: Sempre após concluir alterações no código, testes ou documentação, crie um commit atômico com mensagem clara e descritiva (padrão semântico) e execute `git push` para sincronizar o repositório remoto.
