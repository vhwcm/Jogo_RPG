# Resumo das Alterações: Observabilidade, Logs Estruturados e Documentação Visual D2

Este documento consolida a integração das duas novas preocupações transversais ao projeto **AI RPG Game**, preservando integralmente todas as regras e arquitetura pré-existentes.

---

## 1. O que foi Adicionado

### 📊 A. Observabilidade e Logs Estruturados
1. **Instrumentação Obrigatória**: Toda funcionalidade relevante deve conter logs estruturados nos pontos vitais de execução (início de operações, transições de estado, chamadas de inferência/LLM, erros e exceções).
2. **Contextualização Rica**: Inclusão de metadados padronizados (`campaign_id`, `turn_number`, `action_type`, `provider`, `duration_ms`, `error_type`).
3. **Níveis Semânticos Adequados**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
4. **Segurança (Zero Secrets)**: Proibição estrita de logging de chaves de API (`GEMINI_API_KEY`, etc.), senhas e tokens.
5. **Troubleshooting Baseado em Evidências**: O agente deve obrigatoriamente inspecionar logs de runtime em vez de formular suposições cegas sobre o código.
6. **Procedimentos Reutilizáveis de Troubleshooting**: Documentação de procedimentos conhecidos e recorrentes em `docs/guides/observability_and_troubleshooting.md`.

### 📐 B. Documentação Visual com D2
1. **Padrão D2**: Adoção do formato declarativo D2 para diagramação de fluxos e arquitetura.
2. **Gatilhos de Atualização Visual**: Sempre que uma funcionalidade criar ou alterar fluxos de dados, componentes, fluxos de negócio, integrações externas, processos assíncronos, regras de autenticação ou tratamentos de erro, o diagrama D2 correspondente deve ser criado ou atualizado.
3. **Localização e Referência**: Armazenamento em `docs/diagrams/` e links diretos em documentos Markdown, Specs e ADRs.
4. **Independência Visual**: Permitir a compreensão clara do subsistema sem a necessidade de ler o código-fonte para decifrar a arquitetura.

---

## 2. Arquivos Modificados e Integrados

| Arquivo | Papel e Alteração Realizada |
|---|---|
| [`AGENTS.md`](file:///home/exati/AI_RPG_GAME/AGENTS.md) | Regra-mãe atualizada com as seções de *Observabilidade e Logs Estruturados* e *Documentação Visual com D2*, além da integração no Kiro Flow e regras críticas. |
| [`.agent/rules/architecture.md`](file:///home/exati/AI_RPG_GAME/.agent/rules/architecture.md) | Adição de limites de observabilidade transversal desacoplada e modelagem visual com D2. |
| [`.agent/rules/development.md`](file:///home/exati/AI_RPG_GAME/.agent/rules/development.md) | Inclusão de logs estruturados e diagramas D2 nos fluxos de tarefas (Médias e Grandes) e diretrizes de troubleshooting por evidências. |
| [`.agent/rules/documentation.md`](file:///home/exati/AI_RPG_GAME/.agent/rules/documentation.md) | Adição de D2 na hierarquia de documentação e triggers de sincronia visual. |
| [`.agent/rules/project.md`](file:///home/exati/AI_RPG_GAME/.agent/rules/project.md) | Convenções de logging estruturado (níveis, contexto, segurança zero secrets) e troubleshooting orientado a logs. |
| [`.agent/skills/create-spec/SKILL.md`](file:///home/exati/AI_RPG_GAME/.agent/skills/create-spec/SKILL.md) | Previsão de diagramas D2 e pontos de observabilidade em `design.md` e `tasks.md`. |
| [`.agent/skills/explore-project/SKILL.md`](file:///home/exati/AI_RPG_GAME/.agent/skills/explore-project/SKILL.md) | Consulta aos diagramas D2 em `docs/diagrams/` e inspeção de logs de runtime em diagnósticos. |
| [`.agent/skills/implement-spec/SKILL.md`](file:///home/exati/AI_RPG_GAME/.agent/skills/implement-spec/SKILL.md) | Instrumentação de logs estruturados e geração/atualização dos diagramas D2 durante a codificação. |
| [`.agent/skills/review-consistency/SKILL.md`](file:///home/exati/AI_RPG_GAME/.agent/skills/review-consistency/SKILL.md) | Auditoria cruzada estendida para Diagramas D2 e integridade/segurança dos logs estruturados. |
| [`.agent/skills/update-docs/SKILL.md`](file:///home/exati/AI_RPG_GAME/.agent/skills/update-docs/SKILL.md) | Sincronização obrigatória de diagramas D2 e registro de novos procedimentos de troubleshooting. |
| [`docs/README.md`](file:///home/exati/AI_RPG_GAME/docs/README.md) e [`docs/ARCHITECTURE.md`](file:///home/exati/AI_RPG_GAME/docs/ARCHITECTURE.md) | Atualização do mapa de conhecimento com ADR-006, guias e diagramas D2. |

---

## 3. Novos Artefatos Criados

| Artefato | Finalidade |
|---|---|
| [`docs/decisions/ADR-006-observability-logs-and-d2-visual-documentation.md`](file:///home/exati/AI_RPG_GAME/docs/decisions/ADR-006-observability-logs-and-d2-visual-documentation.md) | Registro arquitetural formal da decisão de adoção de logs estruturados e D2. |
| [`docs/guides/observability_and_troubleshooting.md`](file:///home/exati/AI_RPG_GAME/docs/guides/observability_and_troubleshooting.md) | Guia completo de níveis, padrões de logging e catálogo de procedimentos conhecidos. |
| [`docs/guides/d2_diagrams_guide.md`](file:///home/exati/AI_RPG_GAME/docs/guides/d2_diagrams_guide.md) | Padrões de diagramação e boas práticas de D2. |
| [`docs/diagrams/architecture_layers.d2`](file:///home/exati/AI_RPG_GAME/docs/diagrams/architecture_layers.d2) | Diagrama D2 de camadas limpas e fronteiras do sistema. |
| [`docs/diagrams/turn_execution_flow.d2`](file:///home/exati/AI_RPG_GAME/docs/diagrams/turn_execution_flow.d2) | Diagrama D2 de sequência do ciclo de execução de turnos. |
| [`docs/diagrams/observability_troubleshooting_flow.d2`](file:///home/exati/AI_RPG_GAME/docs/diagrams/observability_troubleshooting_flow.d2) | Diagrama D2 do fluxo de logs e rotina de troubleshooting por agentes. |
