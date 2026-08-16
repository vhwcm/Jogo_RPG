# Requirements: Ativos no Mapa & Hierarquia de Tamanho dos Nós

## Goal
Permitir que itens e ativos do reino (como santuários, estátuas, monumentos, obras, quartéis, fortificações e minas) possuam atributos que indiquem sua capacidade de posicionamento no mapa tático, com sincronização entre inventário/ativos e nós do grafo, além de introduzir uma hierarquia visual de tamanhos e escalas para os nós do mapa (ex: capitais e impérios com destaque e raio maior, vilas e postos médios, santuários e estátuas menores dispostos de forma concêntrica/orbital ao redor do reino).

---

## Functional Requirements

### R1: Atributos de Posicionamento para Ativos do Reino
- O modelo de item/ativo (`Item` / `campaign_items`) deve suportar atributos explícitos de mapa:
  - `posicionavel_no_mapa` (`bool`): indica se o ativo pode ser alocado geograficamente no mapa.
  - `no_mapa` (`bool`): indica se o ativo já foi instanciado como nó no mapa.
  - `map_node_id` (`str`, opcional): identificador único do nó correspondente no grafo do mapa.
  - `tamanho_no` (`str`, opcional: `'mega' | 'grande' | 'medio' | 'pequeno'` ou tier numérico): escala recomendada do nó quando for para o mapa.
  - `camada_mapa` (`str`, opcional: `'estrutura' | 'santuario' | 'obra' | 'fortificacao' | 'monumento'`).

### R2: Hierarquia Visual e Escala de Tamanho dos Nós do Mapa
- O modelo `MapNode` e sua persistência devem suportar definição de escala/tamanho (`size` ou `scale` ou `tier` em `metadata` ou campo dedicado):
  - **Tier Mega / Capital (Raio ~32px)**: Capital do Jogador, Capitais de Reinos Vizinhos/Inimigos.
  - **Tier Grande / Fortalezas & Biomas (Raio ~24px)**: Cidadelas, Grandes Fortalezas, Exércitos Maiores, Biomas Centrais.
  - **Tier Médio / Estruturas & Vilas (Raio ~18px)**: Vilas camponesas, Portos, Minas, Postos Avançados, Acampamentos Militares.
  - **Tier Pequeno / Obras & Santuários (Raio ~13px)**: Santuários, Estátuas, Monumentos, Totens, Ruínas menores, Altares.
- No canvas (`TacticalMap` / `web/js/tactical_map.js`), o cálculo do raio base (`baseRadius`), o tamanho dos ícones/emojis, a espessura do halo/borda e os efeitos de hover devem ser proporcionais ao tamanho/tier do nó.

### R3: Disposição Orbital / Circunferencial de Obras e Santuários ao Redor do Reino
- Quando santuários ou obras periféricas forem criados ou posicionados ao redor do reino, o motor de posicionamento automático deve calcular posições em anéis concêntricos (órbitas táticas) ao redor da Capital (ex: raio de 90px a 140px com distribuição angular harmônica).

### R4: Sincronização e Ações de Posicionamento (Engine & API)
- Suporte a novas ações no `StateManager`:
  - `place_asset_on_map`: posiciona um ativo existente do reino no mapa (gerando ou atualizando o nó correspondente e conectando-o à capital ou nó próximo).
  - `unplace_asset_from_map`: remove o nó do mapa mantendo o item nos ativos do reino com `no_mapa = false`.
- Endpoints REST para controle direto pelo jogador:
  - `POST /api/campaign/{campaign_id}/assets/{asset_id}/place_on_map`
  - `POST /api/campaign/{campaign_id}/assets/{asset_id}/unplace_from_map`

### R5: Interface do Usuário (UI / Web)
- Na aba de **Ativos / Inventário do Reino**, exibir badges indicativas:
  - `[🗺️ Posicionável]` para itens que podem ir ao mapa.
  - `[📍 No Mapa]` com botão de ação rápida para inspecionar/focar a câmera no mapa.
  - Botão de ação `📍 Posicionar no Mapa` para ativos posicionáveis ainda não alocados.
- No mapa tático, permitir filtrar e inspecionar santuários e obras com visualização clara do seu nível hierárquico e vínculo com o ativo.

---

## Non-Functional Requirements
- **Performance**: A renderização no Canvas 2D deve manter 60 FPS estáveis mesmo com dezenas de santuários e obras dispostos ao redor da capital.
- **Retrocompatibilidade**: Campanhas existentes sem os novos atributos devem continuar funcionando normalmente com valores padrão seguros (`default_factory`).
- **Clean Architecture & SOLID**: Separação clara entre camada de domínio puro (`models.py`), persistência SQLite (`schema.py`, `repository.py`), serviços (`state_manager.py`), API (`dto.py`, `app.py`) e frontend vanilla.

---

## Acceptance Criteria
- [ ] Modelos de domínio `Item` e `MapNode` suportam atributos de mapa e hierarquia de tamanho.
- [ ] O banco SQLite persiste e migra com sucesso `campaign_items` e `campaign_map_nodes` mantendo integridade.
- [ ] Nós do mapa no Canvas renderizam com raios, emojis e halos condizentes com sua hierarquia (Capitais maiores, Santuários e Estátuas menores).
- [ ] Ativos como Santuários podem ser posicionados ao redor da capital com layout concêntrico harmônico.
- [ ] Ações de `place_asset_on_map` e `unplace_asset_from_map` funcionam tanto via IA/Turno quanto via API/UI.
- [ ] Todos os testes automatizados (`pytest`) passam com 100% de sucesso e sem comentários no código.
