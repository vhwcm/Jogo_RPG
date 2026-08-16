# 🗄️ Database Architecture (SQLite3 & Vector Store)

## 1. Visão Geral
O sistema utiliza **SQLite3** embutido, configurado para alta performance e confiabilidade através de:
- `journal_mode = WAL` (Write-Ahead Logging) para permitir leituras concorrentes durante escritas.
- `PRAGMA foreign_keys = ON` com cláusulas `ON DELETE CASCADE` em todas as tabelas filhas.
- `conn.row_factory = sqlite3.Row` com conversão para dicionários na camada de repositório.

---

## 2. Diagrama de Relacionamento de Tabelas (ERD)

```
┌───────────────────────────────────────────────┐
│                   campaigns                   │
├───────────────────────────────────────────────┤
│ id (PK)                                       │
│ name                                          │
│ summary (Capítulos comprimidos)               │
│ created_at                                    │
│ updated_at                                    │
└──────┬────────────┬────────────┬───────────┬──┘
       │            │            │           │
       ▼ (1:N)      ▼ (1:N)      ▼ (1:N)     ▼ (1:N)
┌──────────────┐ ┌────────────┐ ┌─────────┐ ┌──────────┐
│ world_state  │ │ characters │ │ quests  │ │ memories │
├──────────────┤ ├────────────┤ ├─────────┤ ├──────────┤
│ id (PK)      │ │ id (PK)    │ │ id (PK) │ │ id (PK)  │
│ campaign_id  │ │ campaign_id│ │ campaign│ │ campaign │
│ turn_number  │ │ name       │ │ title   │ │ turn_num │
│ kingdom_name │ │ role       │ │ desc    │ │ content  │
│ ruler_name   │ │ location   │ │ status  │ │ importnce│
│ race         │ │ is_alive   │ │ reward  │ │ embed_js │
│ gold         │ │ relation   │ └─────────┘ │ char_js  │
│ population   │ │ knowl_json │             └──────────┘
│ military     │ └────────────┘
│ happiness    │
│ religion     │
└──────────────┘
```

---

## 3. Descrição das Tabelas

### `campaigns`
Armazena a entidade raiz da campanha e o sumário acumulado de capítulos gerado pelo `CampaignSummarizer`.

### `world_state`
Registra o snapshot determinístico dos recursos do reino a cada turno (`turn_number`). Permite análise de evolução e execução de rollbacks seguros.

### `characters`
Guarda NPCs e figuras importantes descobertas ou interagidas durante a aventura, seu papel, localização, lealdade (`relationship_with_player`) e fatos conhecidos (`knowledge_json`).

### `quests`
Registra objetivos ativos, pendentes ou concluídos com suas respectivas metas e recompensas.

### `items` & `locations`
Tabelas auxiliares para inventário do reino e locais descobertos no mapa mundi.

### `campaign_map_nodes` & `campaign_map_edges`
Armazena os vértices e arestas do mapa tático e grafo territorial:
- `id`, `campaign_id`, `label`, `node_type`, `emoji`, `x`, `y`, `status`.
- `size`: Escala hierárquica do nó (`mega`, `grande`, `medio`, `pequeno`, `micro`).
- `metadata_json`: Metadados operacionais e vínculos com ativos (`asset_id`).

### `memories` (Vector Store)
Armazena as memórias episódicas do jogo:
- `content`: Texto descritivo do acontecimento.
- `importance`: Score flutuante de 0.0 a 1.0 atribuído na criação.
- `embedding_json`: Vetor de embedding serializado em JSON.
- `characters_json`: Lista de nomes de personagens associados ao evento para filtragem relacional.

---

## 4. Migrations & Evolução de Schema
As migrações são gerenciadas em `engine/db/schema.py` na função `init_db()`.
- Criação condicional com `CREATE TABLE IF NOT EXISTS`.
- Adição idempotente de colunas via `PRAGMA table_info` antes de executar `ALTER TABLE ADD COLUMN`.
