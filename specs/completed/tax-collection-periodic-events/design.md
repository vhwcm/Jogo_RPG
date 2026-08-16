# Design: Recolhimento de Impostos & Motor de Fórmulas Determinísticas

## Arquitetura e Componentes

### 1. Camada de Domínio (`engine/domain/`)

#### 1.1 `FormulaEvaluator` (`engine/domain/formula_evaluator.py`)
Módulo puro de avaliação matemática baseado no módulo padrão `ast` do Python:
- Operadores suportados: `Add`, `Sub`, `Mult`, `Div`, `FloorDiv`, `Mod`, `USub`, `UAdd`.
- Funções seguras permitidas: `min`, `max`, `round`, `int`, `float`, `abs`.
- Contexto de variáveis:
  - `populacao`: `int`
  - `felicidade`: `float` (convertido de `"70%"` -> `70.0`, ou `0.70` dependendo da expressão)
  - `dinheiro` / `ouro`: `int`
  - `poder_militar`: `int`
  - `dia_atual`: `int`
- Método `evaluate_formula(formula: str, context: Dict[str, Any]) -> float`
- Método `calculate_event_effect(efeito: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, int]`

#### 1.2 Atualização no `PeriodicEvent` (`engine/domain/models.py`)
Garantir que a estrutura do evento suporte fórmulas no dicionário `efeito` com campos:
- `formula`: string com a expressão (ex: `"(populacao * 0.05) * (felicidade / 100)"`)
- `recurso`: chave do recurso afetado (ex: `"dinheiro"`)
- `aliquota`: valor numérico opcional (ex: `0.05`)
- `descricao_calculo`: texto descritivo

#### 1.3 `ActionEvaluator` e `GameEngine` (`engine/domain/state_manager.py`)
- Em `create_campaign`:
  - Registrar evento padrão `pe_recolhimento_impostos` com intervalo de 30 dias e fórmula determinística.
- Em `_process_turn_response`:
  - Antes de persistir o novo estado, buscar eventos devidos (`get_due_periodic_events(campaign_id, current_day)` ou `evaluation_result.eventos_periodicos_disparados`).
  - Para cada evento disparado:
    - Executar `calculate_event_effect` com o estado atual.
    - Aplicar deltas ao `final_gold`, `final_mil`, etc.
    - Atualizar `proximo_disparo_dia` e `ultimo_disparo_dia`.
- Em `ContextBuilder`:
  - Enriquecer as diretrizes com o resultado detalhado do recolhimento de impostos para que o LLM narre o evento fielmente.

---

### 2. Camada de API (`server/app.py` & DTOs)
- Endpoint `GET /api/campaign/{campaign_id}/events` retorna os eventos com cálculos e projeções atuais.
- Endpoint `POST /api/campaign/{campaign_id}/events/{event_id}/calculate` para simular/avaliar a fórmula com base no estado do reino.

---

### 3. Interface Web (`web/js/ui.js` e `web/js/app.js`)
- Renderização de badges e projeção no cartão de eventos periódicos.
- Visualização do próximo recolhimento e valor estimado de arrecadação em ouro.

---

### 4. Tratamento de Erros & Segurança
- `FormulaEvaluator` rejeita nós AST não permitidos (`Call` a funções não autorizadas, `Import`, `Attribute`, etc.), lançando exceções controladas ou retornando 0 com log seguro.
- Falhas na avaliação de fórmula não travam a execução do turno; um fallback seguro (0 de delta) é aplicado.
