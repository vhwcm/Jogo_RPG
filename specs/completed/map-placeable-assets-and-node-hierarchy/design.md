# Design: Ativos no Mapa & Hierarquia de Tamanho dos Nós

## Architecture & Overview
A funcionalidade estende a integração entre o sistema de inventário de ativos do reino (`campaign_items`) e o grafo espacial tático (`campaign_map_nodes` e `campaign_map_edges`), proporcionando:
1. Metadados de posicionabilidade e ligação bidirecional entre itens e nós do mapa.
2. Definição de escala/tamanho padronizada de nós do mapa (`mega`, `grande`, `medio`, `pequeno`), garantindo diferenciação visual no renderizador Canvas 2D.
3. Algoritmo de posicionamento orbital concêntrico para estruturas periféricas ao redor do reino (como santuários e monumentos).

---

## Domain Models (`engine/domain/models.py`)

### Atualizações em `MapNode`:
```python
@dataclass
class MapNode:
    id: str
    label: str
    node_type: str = "estrutura"
    emoji: str = "📍"
    x: float = 0.0
    y: float = 0.0
    status: str = "ativo"
    size: str = "medio"
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### Atualizações nos atributos de `Item`:
Os atributos do dicionário `atributos: Dict[str, Any]` em `Item` recebem convenções padronizadas:
- `posicionavel_no_mapa: bool` (default: `False` para itens comuns; `True` para santuários, obras, estátuas, fortificações, templos, etc.)
- `no_mapa: bool` (default: `False`)
- `map_node_id: Optional[str]`
- `tamanho_no: str` (`"pequeno" | "medio" | "grande" | "mega"`)
- `raio_orbital: Optional[float]` (distância recomendada da capital quando posicionado)

---

## Database Changes (`engine/db/`)

### 1. `engine/db/schema.py`
- Adicionar coluna `size TEXT DEFAULT 'medio'` na tabela `campaign_map_nodes` caso não exista via migração PRAGMA table_info no `init_db`.
- Tabela `campaign_items` já suporta `atributos_json TEXT DEFAULT '{}'`, onde os metadados `posicionavel_no_mapa`, `no_mapa`, `map_node_id`, `tamanho_no` serão armazenados com integridade e deserializados.

### 2. `engine/db/repository.py`
- Atualizar `upsert_map_node` para aceitar parâmetro `size: str = "medio"`.
- Atualizar `get_map_nodes` para retornar o campo `size`.
- Criar método auxiliar `link_item_to_map_node(item_id: str, campaign_id: str, node_id: str)` e `unlink_item_from_map_node(item_id: str, campaign_id: str)`.

---

## Engine & State Manager (`engine/domain/state_manager.py`)

### 1. Detecção e classificação automática de ativos:
- Ao receber `add_structure`, `add_kingdom_asset` ou `add_item`:
  - Se a categoria for `'estrutura'`, `'santuario'`, `'obra'`, `'monumento'`, `'fortificacao'`, `'estatua'` ou o nome contiver termos correspondentes, marcar `posicionavel_no_mapa = True` e definir `tamanho_no` adequado (ex: santuário/estátua -> `"pequeno"`, fortificação -> `"grande"`, capital/reino -> `"mega"`).
  - Se vier com flag de posicionamento imediato ou coordenadas, criar automaticamente o `MapNode` e a aresta (`MapEdge`) conectando à capital.

### 2. Algoritmo Orbital de Posicionamento ao redor do Reino:
- Função `calculate_orbital_position(campaign_id, node_type, index)`:
  - Distribui santuários e pequenas obras em órbitas concêntricas (ex: anel interno r=95px, anel intermediário r=140px, anel externo r=185px) ao redor da capital `(0, 0)`.
  - Calcula ângulo baseado no número de nós existentes naquele anel para evitar sobreposição (`collision avoidance`).

### 3. Ações no `StateManager`:
- `place_asset_on_map`: cria nó e aresta com tipo e tamanho corretos, atualiza o item com `no_mapa = True` e `map_node_id`.
- `unplace_asset_from_map`: remove nó e arestas, atualiza o item com `no_mapa = False` e `map_node_id = None`.

---

## API & DTOs (`server/`)

### Novos DTOs (`server/dto.py`):
```python
class PlaceAssetRequest(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    node_type: Optional[str] = None
    size: Optional[str] = None
    connect_to_capital: bool = True
```

### Novos Endpoints (`server/app.py`):
- `POST /api/campaign/{campaign_id}/assets/{asset_id}/place_on_map`
- `POST /api/campaign/{campaign_id}/assets/{asset_id}/unplace_from_map`

---

## Presentation / Web (`web/`)

### 1. `web/js/tactical_map.js`
- Mapeamento de tamanhos e raios base:
  ```javascript
  nodeSizes: {
      'mega': 32,
      'grande': 24,
      'medio': 18,
      'pequeno': 13,
      'micro': 10
  }
  ```
- O cálculo de `baseRadius` considerará:
  1. `node.size` explícito se fornecido.
  2. Fallback baseado no `node_type` (ex: `capital` -> 32, `reino_vizinho` -> 28, `exercito` -> 22, `santuario`/`ruina`/`estatua` -> 13).
- O tamanho da fonte do emoji/ícone será proporcional ao raio (`Math.round(baseRadius * 1.1)px`).
- Halos e bordas adaptadas para nós pequenos não ficarem poluídos visualmente.

### 2. `web/js/ui.js` e `web/css/components.css`
- Renderização na lista de Ativos do Reino:
  - Tag visual `[🗺️ Posicionável]` ou `[📍 No Mapa]`.
  - Botão de ação `📍 Posicionar no Mapa` / `Focar no Mapa`.
- No clique de um nó do mapa correspondente a um ativo, exibir no painel lateral/tooltip detalhes do ativo associado.

---

## Error Handling & Edge Cases
- Se um item for deletado enquanto estiver no mapa, o nó correspondente é limpo defensivamente sem deixar arestas órfãs.
- Se as coordenadas fornecidas forem inválidas, o algoritmo orbital calcula coordenadas válidas automaticamente.
- Se o banco contiver registros antigos sem o campo `size`, o valor padrão `'medio'` é assumido de forma transparente.

---

## Testing Strategy
- Teste unitário de criação e migração do campo `size` em `test_db.py`.
- Teste unitário de vinculação e posicionamento de ativos no mapa em `test_map_graph.py` e `test_actions.py`.
- Teste de endpoints REST em `test_api.py`.
