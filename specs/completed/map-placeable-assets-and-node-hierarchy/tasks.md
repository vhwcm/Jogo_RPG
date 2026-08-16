# Tasks: Ativos no Mapa & Hierarquia de Tamanho dos Nós

## Checklist de Implementação

- [x] **1. Persistência & Schema**:
  - [x] 1.1 Atualizar `engine/db/schema.py` com coluna `size` em `campaign_map_nodes` e migração PRAGMA.
  - [x] 1.2 Atualizar `engine/db/repository.py` com suporte ao campo `size` em `upsert_map_node` e `get_map_nodes`.
  - [x] 1.3 Adicionar métodos de vinculação de item/ativo a nó de mapa em `repository.py`.
- [x] **2. Domínio & Engine**:
  - [x] 2.1 Atualizar `MapNode` em `engine/domain/models.py` com campo `size: str = "medio"`.
  - [x] 2.2 Implementar lógica de classificação de ativos posicionáveis e tamanhos em `engine/domain/state_manager.py`.
  - [x] 2.3 Implementar algoritmo de posicionamento orbital concêntrico ao redor da capital para santuários e obras.
  - [x] 2.4 Implementar handlers para ações `place_asset_on_map` e `unplace_asset_from_map` no `StateManager`.
- [x] **3. API & DTOs**:
  - [x] 3.1 Adicionar DTO `PlaceAssetRequest` em `server/dto.py`.
  - [x] 3.2 Implementar rotas `POST /api/campaign/{campaign_id}/assets/{asset_id}/place_on_map` e `unplace_from_map` em `server/app.py`.
- [x] **4. Interface & Apresentação (Tactical Map & UI)**:
  - [x] 4.1 Atualizar `web/js/tactical_map.js` para renderizar nós com raios, tamanhos de fonte e halos baseados na hierarquia (`mega`, `grande`, `medio`, `pequeno`).
  - [x] 4.2 Atualizar `web/js/ui.js` e `web/js/app.js` para exibir badges de posicionamento e botões de ação nos ativos do reino.
  - [x] 4.3 Ajustar estilos em `web/css/components.css` para tags e controles de ativos no mapa.
- [x] **5. Testes & Qualidade (TDD)**:
  - [x] 5.1 Adicionar testes unitários em `tests/test_map_graph.py` e `tests/test_actions.py` cobrindo hierarquia de tamanho e posicionamento de ativos.
  - [x] 5.2 Adicionar testes de API em `tests/test_api.py`.
  - [x] 5.3 Executar `pytest` e garantir 100% de passagem sem erros ou regressões.
- [x] **6. Documentação & Review**:
  - [x] 6.1 Executar skill `review-consistency`.
  - [x] 6.2 Executar skill `update-docs` para atualizar `docs/domain/`, `docs/systems/` e `docs/architecture/`.
  - [x] 6.3 Mover a spec para `specs/completed/map-placeable-assets-and-node-hierarchy/`.
