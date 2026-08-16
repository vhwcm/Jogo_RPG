# Resumo de Alterações: Ativos no Mapa & Hierarquia de Tamanho dos Nós

## 📌 Contexto e Motivação
Muitos dos ativos do reino (como santuários, estátuas, monumentos, obras e fortificações) precisam estar visíveis e posicionados no mapa tático ao redor do reino. Além disso, os nós do mapa não devem ter todos o mesmo tamanho: o nó central da capital do jogador e dos impérios vizinhos deve ser consideravelmente maior do que os nós de estátuas, santuários ou pequenos marcos.

---

## 🛠️ O que foi Implementado

### 1. Hierarquia Visual de Nós no Canvas (`web/js/tactical_map.js`)
- **Tamanhos e Raios Proporcionais**:
  - `mega` (32px): Capital do reino e capitais de reinos vizinhos (com duplo halo pulsante).
  - `grande` (24px): Biomas (Floresta, Montanha, Planície) e grandes fortalezas.
  - `medio` (18px): Vilas, minas, portos e postos avançados.
  - `pequeno` (13px): Santuários, estátuas, monumentos, obras menores e altares.
- Fontes de emojis, halos, espessura de bordas e badges de status adaptados automaticamente ao tamanho do nó para manter a legibilidade sem poluição visual.
- Método `TacticalMap.focusNode(nodeId)` para recentralizar a câmera tática e abrir a inspeção do nó com zoom suave.

### 2. Ativos Posicionáveis e Sincronização de Inventário
- Atributos padronizados nos itens do reino (`Item.atributos`):
  - `posicionavel_no_mapa`: `True` para santuários, obras, estátuas, fortificações, etc.
  - `no_mapa`: `True` quando alocado no mapa.
  - `map_node_id`: ID do nó correspondente no grafo territorial.
  - `tamanho_no`: Escala do nó (`pequeno`, `medio`, `grande`, `mega`).
- **Algoritmo de Distribuição Orbital Concêntrica**:
  - Santuários e estátuas posicionados ao redor do reino são organizados em órbitas harmônicas concêntricas (raios de 95px, 140px e 185px ao redor da capital) com verificação angular de slots para evitar sobreposições.

### 3. Camada de Domínio, Persistência e API
- **Banco SQLite (`engine/db/schema.py` e `repository.py`)**:
  - Coluna `size TEXT DEFAULT 'medio'` em `campaign_map_nodes` com migração PRAGMA.
  - Métodos `link_item_to_map_node` e `unlink_item_from_map_node`.
- **Engine (`engine/domain/state_manager.py`)**:
  - Funções `_infer_node_size`, `_is_placeable_asset` e `_calculate_orbital_position`.
  - Ações no motor: `place_asset_on_map` e `unplace_asset_from_map`.
- **API REST (`server/app.py` e `server/dto.py`)**:
  - `POST /api/campaigns/{campaign_id}/assets/{asset_id}/place_on_map`
  - `POST /api/campaigns/{campaign_id}/assets/{asset_id}/unplace_from_map`

### 4. Interface do Usuário (`web/js/ui.js`, `web/js/app.js` e `web/css/components.css`)
- Badges visuais `[📍 No Mapa]` e `[🗺️ Posicionável]`.
- Botões de ação rápida para posicionar no mapa ou focar câmera no nó existente.

---

## 🧪 Validação
- **Testes Automatizados**: 55 de 55 testes passaram com 100% de sucesso no `pytest`.
- **Regras do Projeto**: Zero comentários adicionados no código-fonte.
