# Resumo das Alterações: Arquitetura Two-Tier de Arbitragem Semântica, Calendário em Dias e Eventos Periódicos

## 1. Visão Geral

Foi implementada uma reformulação arquitetural profunda no motor do jogo para resolver os problemas de imediatismo narrativo, falta de consolidação de custos em ações combinadas (ex: "quero fazer 1 e 2") e ausência de progressão temporal determinística.

---

## 2. Componentes e Alterações Implementadas

### A. Árbitro Semântico Especializado (`engine/domain/evaluator.py`)
- Criada a classe `ActionEvaluator`, responsável por avaliar semanticamente qualquer intenção do jogador antes da geração narrativa.
- Executa em baixa temperatura (`temperature=0.1`) com prompt estrito de arbitragem de regras.
- Mapeia intenções com opções numéricas ou mistas, somando custos de ouro, poder militar e população.
- Valida viabilidade de recursos contra o estado atual do reino.
- Estima o tempo transcorrido em dias (`dias_passados`) e classifica as ações entre `imediata` e `longo_prazo`.
- Bloqueia a conclusão prematura de quests de longo prazo, instruindo o narrador a descrever apenas os preparativos ou mobilização inicial.

### B. Calendário do Reino e Hooks Temporais no Banco de Dados (`engine/db/`)
- **`engine/db/schema.py`**:
  - Adicionada coluna `current_day` na tabela `world_state`.
  - Adicionadas colunas `dia_inicio` e `dias_estimados` na tabela `campaign_tasks`.
  - Adicionada tabela `periodic_events` (`id`, `campaign_id`, `titulo`, `intervalo_dias`, `ultimo_disparo_dia`, `proximo_disparo_dia`, `efeito_json`, `status`, `criado_no_turno`).
- **`engine/db/repository.py`**:
  - Métodos CRUD para `periodic_events` (`upsert_periodic_event`, `get_periodic_events`, `get_due_periodic_events`, `delete_periodic_event`).
  - Suporte completo a `current_day`, `dia_inicio` e `dias_estimados` em consultas e snapshots históricos.

### C. Context Builder & Prompting (`engine/memory/context_builder.py`)
- Injeção da seção `=== CALENDÁRIO E TEMPO DO REINO ===` com contagem do Dia Atual e Dias Passados.
- Injeção da seção `=== DIRETRIZES OBRIGATÓRIAS DO ÁRBITRO DE REGRAS ===` que força o narrador criativo a respeitar estritamente os deltas de recursos calculados e a regra de não conclusão imediata para tarefas de longo prazo.
- Injeção da seção `=== EVENTOS PERIÓDICOS E CRONOGRAMA DO REINO ===` para visibilidade de tributos e eventos recorrentes.

### D. Game Engine & State Manager (`engine/domain/state_manager.py`)
- Orquestração em duas etapas em `execute_turn`:
  1. Avaliação pelo `ActionEvaluator`.
  2. Construção do contexto enriquecido e execução do `GameMaster`.
- Processamento de novas actions modulares: `create_periodic_event`, `update_periodic_event`, `remove_periodic_event`.
- Aplicação automática de efeitos de eventos periódicos com prazos vencidos e reagendamento do próximo disparo (`proximo_disparo_dia = current_day + intervalo_dias`).
- Atualização do endpoint `/estimate_action` para fornecer prévia com soma de custos e estimativa de dias em tempo real.

### E. DTOs & Contratos de API (`server/dto.py`)
- `KingdomStatusDTO`: adicionados `dia_atual` e `dias_passados`.
- `TaskDTO`: adicionados `dia_inicio` e `dias_estimados`.
- `PeriodicEventDTO`: modelo completo para serialização de eventos recorrentes.
- `StateDetailsDTO`: inclui lista de `periodic_events`.

### F. Interface Web & HUD do Reino (`web/`)
- **HUD Superior**:
  - Exibição de calendário: `📅 Dia X (Ano Y, Dia Z)`.
  - Badge animado com destaque do tempo transcorrido (`+N dias`).
- **Drawer de Eventos Periódicos & Cronograma**:
  - Novo botão e modal dedicado para visualização de tributos, manutenções, intervalos em dias e contagem regressiva para o próximo disparo.
- **Prévia de Ações (Preflight Estimate)**:
  - Exibição dos custos consolidados (ouro e militar), dias estimados (`📅 +N dias`), selo de `⏳ Longo Prazo` e alerta de `⚠️ Inviável` quando faltarem recursos.

---

## 3. Validação e Testes Automatizados

- Criada suíte `tests/test_evaluator.py` validando combinação de opções ("1 e 2"), inviabilidade de recursos e estimativa de dias.
- Criada suíte `tests/test_periodic_events.py` validando persistência SQLite, avanço temporal e disparo de eventos periódicos.
- Suíte completa do projeto (`pytest`) com **51 testes passando com 100% de sucesso**.
