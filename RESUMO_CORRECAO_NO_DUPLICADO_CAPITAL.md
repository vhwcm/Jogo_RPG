# Resumo da Correção: Prevenção e Limpeza de Nó Duplicado da Capital / Reino Vizinho

## Problema Identificado
O reino do jogador (ex: `Valdrin`), cuja capital oficial já reside de forma canônica no centro do mapa (`node_capital`, posição `(0.0, 0.0)`, tipo `capital`), estava sendo inserido adicionalmente no grafo como um nó extra (`capital_valdrin`) e categorizado erroneamente como `reino_vizinho` com posição orbital deslocada (sobrepondo outros nós como a Floresta Ancestral).

Isso ocorria quando o modelo de linguagem ou o fluxo emitia uma ação `add_map_node` ou `add_ally` referenciando a própria capital ou o nome do reino do jogador.

## Alterações Realizadas

### 1. Sanitização e Validação no Backend (`engine/domain/state_manager.py`)
- **`_is_player_kingdom_or_capital`**: Método que identifica todas as variações nominais do reino, soberano e capital do jogador (ex: `Valdrin`, `Capital Valdrin`, `Valdrin (Capital)`, `Reino de Valdrin`, `capital_valdrin`, etc.).
- **`apply_actions`**:
  - **`add_ally` / `update_ally`**: Bloqueia e descarta tentativas de cadastrar o próprio reino do jogador como aliado ou império vizinho externo.
  - **`add_map_node` / `update_map_node`**: Impede a criação de nós secundários ou categorização como `reino_vizinho` para o reino do jogador. Se uma ação tentar adicionar/atualizar a capital, ela direciona as atualizações de metadados para o nó canônico `node_capital` mantendo sua posição central fixa em `(0.0, 0.0)` e tipo `capital`.
- **`_cleanup_duplicate_capital_nodes` & `get_campaign_state_details`**: Limpeza automática e contínua de quaisquer nós de capital duplicados ou nós espúrios de `reino_vizinho` do próprio jogador existentes no banco de dados.

### 2. Diretrizes dos Prompts e Contexto (`state_manager.py` & `context_builder.py`)
- Inclusão de regra explícita nas instruções do sistema (`SYSTEM_PROMPT`) e no construtor de contexto (`ContextBuilder`):
  - O reino e a capital do jogador já residem centralizados no mapa.
  - O modelo é expressamente proibido de emitir `add_ally` ou `add_map_node` do tipo `reino_vizinho` para o próprio reino do jogador.

### 3. Sanitização Defensiva no Frontend (`web/js/tactical_map.js`)
- Em `TacticalMap.setData`, adicionado filtro defensivo que descarta nós duplicados de capital ou nós de `reino_vizinho` com o nome do reino do jogador, garantindo consistência visual e removendo arestas órfãs.

### 4. Limpeza do Banco de Dados Ativo (`data/rpg_game.db`)
- Executada rotina de higienização que expurgou o nó `capital_valdrin` e arestas associadas da campanha principal ativa.

### 5. Cobertura de Testes Automatizados (`tests/test_map_graph.py`)
- **`test_prevent_player_kingdom_as_neighbor_or_duplicate_capital`**: Valida que ações de `add_ally` e `add_map_node` com o nome do reino do jogador não criam nós de `reino_vizinho` nem duplicam a capital.
- **`test_cleanup_existing_duplicate_capital_nodes`**: Valida a purga automática de nós espúrios ao consultar os detalhes da campanha.
