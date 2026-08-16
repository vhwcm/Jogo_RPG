# Tasks: Recolhimento de Impostos & Cálculo Determinístico

- [x] **Task 1: Implementar `FormulaEvaluator` e Testes Unitários de Domínio**
  - [x] Criar `tests/test_formula_evaluator.py` com testes para avaliação de expressões, contexto de reino, segurança contra código malicioso e parsing de felicidade ("70%", 70, 0.7).
  - [x] Implementar `engine/domain/formula_evaluator.py` utilizando `ast` seguro (sem comentários no código).

- [x] **Task 2: Integrar Inicialização do Evento de Impostos no Início da Aventura**
  - [x] Escrever teste em `tests/test_periodic_events.py` verificando que `create_campaign` registra o evento `"recolhimento_impostos"` para o dia 30 com a fórmula matemática configurada.
  - [x] Atualizar `create_campaign` em `engine/domain/state_manager.py` para registrar o evento padrão.

- [x] **Task 3: Implementar Execução e Aplicação Determinística no Fluxo de Turnos**
  - [x] Escrever teste de transição de turno verificando que, quando o dia ultrapassa 30, o evento dispara, calcula `(populacao * 0.05) * (felicidade / 100)` e credita o ouro no estado do reino, avançando o próximo disparo para o dia 60.
  - [x] Atualizar `ActionEvaluator` e `_process_turn_response` no `engine/domain/state_manager.py` para avaliar fórmulas e aplicar os deltas calculados no estado do reino.
  - [x] Atualizar `ContextBuilder` para narrar o recolhimento com os números exatos arrecadados.

- [x] **Task 4: Suportar Modificação e Evolução de Impostos via Ações**
  - [x] Testar alteração de alíquota/fórmula via `update_periodic_event` (ex: aumento de impostos para 8%).
  - [x] Garantir que o `apply_actions` atualize a fórmula e que o próximo recolhimento utilize o novo cálculo.

- [x] **Task 5: Atualizar Interface Web (UI) e Projeções de Eventos**
  - [x] Atualizar `web/js/ui.js` para exibir a fórmula do evento e a projeção estimada de arrecadação em ouro baseada na população e felicidade atuais.

- [x] **Task 6: Validação Completa, Testes e Sincronização de Docs**
  - [x] Executar toda a suíte de testes `pytest` garantindo 100% de sucesso.
  - [x] Atualizar documentação em `docs/domain/` e `docs/systems/`.
  - [x] Mover spec de `specs/active/` para `specs/completed/`.
  - [x] Realizar commit semântico e push no repositório.
