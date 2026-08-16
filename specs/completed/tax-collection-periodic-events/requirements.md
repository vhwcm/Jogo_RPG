# Requirements: Recolhimento de Impostos & Cálculo Determinístico em Eventos Periódicos

## Goal
Implementar o evento periódico inicial "Recolhimento de Impostos" configurado a cada 30 dias em todas as novas campanhas, com suporte a um motor de cálculo matemático determinístico dinâmico baseado no estado do reino (população e felicidade), permitindo evolução de alíquotas e fórmulas ao longo do tempo.

---

## Functional Requirements

### R1: Evento Inicial Automático de Recolhimento de Impostos
- No momento da criação de qualquer nova campanha (`create_campaign`), um evento periódico padrão deve ser registrado automaticamente com os seguintes dados:
  - `id`: `"pe_recolhimento_impostos"`
  - `titulo`: `"Recolhimento de Impostos"`
  - `intervalo_dias`: `30`
  - `proximo_disparo_dia`: `30`
  - `status`: `"ativo"`
  - `descricao`: `"Arrecadação periódica de tributos reais com base na população e no índice de felicidade do reino."`
  - `efeito`:
    - `formula`: `"(populacao * 0.05) * (felicidade / 100)"`
    - `recurso`: `"dinheiro"`
    - `aliquota`: `0.05`

### R2: Motor de Cálculo Matemático Determinístico
- Criar um avaliador de fórmulas seguro e determinístico (`engine/domain/formula_evaluator.py`) que:
  - Suporte variáveis do reino: `populacao` (int), `felicidade` (float 0..100 extraído de strings como "70%"), `dinheiro` (int), `poder_militar` (int), `dia_atual` (int).
  - Avalie expressões matemáticas padrão (`+`, `-`, `*`, `/`, `(`, `)`, `%`, `round`, `int`, `min`, `max`) sem uso de `eval()` inseguro (usando AST parsing seguro).
  - Retorne valores inteiros arredondados ou deltas determinísticos aplicáveis a recursos do reino.

### R3: Disparo e Aplicação Determinística em Turnos
- Durante o avanço de tempo (`execute_turn` e `_process_turn_response`):
  - Identificar eventos periódicos ativos que atingiram o dia de disparo (`proximo_disparo_dia <= current_day`).
  - Para cada evento disparado:
    - Avaliar a fórmula matemática determinística utilizando o estado atual do reino.
    - Calcular o delta exato de recursos (ex: `+350` de dinheiro para 10.000 habitantes e 70% de felicidade).
    - Aplicar o delta diretamente aos recursos do reino (`final_gold`).
    - Agendar o próximo disparo (`proximo_disparo_dia += intervalo_dias`).
    - Atualizar `ultimo_disparo_dia = current_day`.
    - Injetar no contexto do Narrador (`ContextBuilder`) a discriminação exata da arrecadação ocorrida.

### R4: Mutabilidade e Evolução das Fórmulas ao Longo da Campanha
- Suporte para atualização de fórmulas e alíquotas via action `update_periodic_event` emitida pelo Game Master ou por decisões do jogador (ex: decreto real aumentando impostos para 8%).
- Endpoints REST para inspeção e atualização de eventos periódicos e simulação de cálculos.

### R5: Visualização e Estimativa na Interface Web
- No painel de Eventos da interface web (`web/js/ui.js`):
  - Exibir a tag de fórmula/cálculo dinâmico (ex: `💰 Fórmula: 5% da População × Felicidade`).
  - Exibir a estimativa de arrecadação baseada no estado atual do reino (ex: `Projeção: +350 ouro`).

---

## Non-Functional Requirements
- **Segurança**: Expressões matemáticas devem ser analisadas via AST seguro sem execução de código arbitrário.
- **Determinismo**: Resultados matemáticos devem ser 100% reproduzíveis dado o mesmo estado do reino.
- **Clean Architecture**: Regras de domínio e fórmulas isoladas em `engine/domain/`, desacopladas de frameworks web e LLMs.
- **TDD e Sem Comentários**: Implementação guiada por testes com 100% de aprovação e zero comentários no código.

---

## Acceptance Criteria
- [ ] Nova campanha inicia com o evento "Recolhimento de Impostos" cadastrado para o dia 30.
- [ ] Fórmula `(populacao * 0.05) * (felicidade / 100)` é calculada com precisão determinística (ex: pop 10000, felicidade 70% = +350 ouro).
- [ ] Ao avançar 30+ dias, o evento dispara, o ouro é adicionado e o próximo disparo é reagendado para o dia 60+.
- [ ] Alterações na fórmula ou alíquota via action são persistidas e refletem no próximo disparo.
- [ ] Todos os testes unitários e de integração passam no `pytest`.
