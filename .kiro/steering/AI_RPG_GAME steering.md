---
inclusion: always
---

# AI RPG Game — Project Steering

## Project Overview

A medieval/fantasy AI-driven RPG where the player rules a kingdom. Each turn the player submits a free-text action and the LLM generates a narrative response plus updated kingdom stats. The system combines a FastAPI REST server, a web UI, a CLI, and a standalone terminal client.

## Architecture

Clean, layered Python architecture:

```
config.py              — All settings, loaded from .env via python-dotenv
engine/
  domain/
    models.py          — Pure dataclasses: KingdomStatus, TurnResponse, CampaignInfo, OpcaoDecisao, ImpactoPrevisto
    state_manager.py   — GameEngine: orchestrates campaigns, turns, rollbacks, import/export
  db/
    schema.py          — SQLite3 DDL + init_db(), get_connection() with WAL mode
    repository.py      — Repository: all SQL CRUD (campaigns, world_state, characters, quests, items, locations)
    vector_store.py    — VectorStore: episodic memory with cosine-similarity RAG search
  memory/
    context_builder.py — ContextBuilder: assembles full LLM prompt from structured state + RAG + short-term history
    importance.py      — calculate_importance(): scores a memory string for relevance
    summarizer.py      — CampaignSummarizer: periodic chapter summarisation via LLM
  providers/
    base.py            — BaseLLMProvider ABC (generate_text, generate_json, generate_embedding, is_available, name)
    gemini_provider.py — Google Gemini (default)
    grok_provider.py   — xAI Grok
    openai_provider.py — OpenAI
    ollama_provider.py — Local Ollama
    factory.py         — LLMFactory.get_provider() → FallbackLLMProvider wrapping primary + all others
server/
  app.py               — FastAPI app, all REST endpoints
  dto.py               — Pydantic DTOs for request/response
cli/main.py            — Rich-based interactive CLI
terminal_rpg/rpg.py    — Standalone terminal client (separate entry point)
run.py                 — Main entry point (launches server + optional web UI)
data/rpg_game.db       — SQLite3 database
```

## Key Conventions

### Python Style
- Python 3.10+; use type hints on all function signatures.
- Use `dataclasses` for domain models (`engine/domain/models.py`); use Pydantic `BaseModel` for DTOs (`server/dto.py`).
- Domain models and business logic live exclusively in `engine/`; the `server/` layer only handles HTTP and DTO translation.
- No business logic in `server/app.py` — delegate everything to `GameEngine`.
- All configuration comes from `config.py`; never hardcode API keys, paths, or model names elsewhere.
- The `.env` file at the project root holds secrets; `config.py` loads it, never read `.env` directly.

### LLM Provider Pattern
- All providers implement `BaseLLMProvider` from `engine/providers/base.py`.
- Always obtain a provider through `LLMFactory.get_provider(name)`, which returns a `FallbackLLMProvider` (tries the named provider first, then falls back through the rest, finally `MockFallbackProvider`).
- `generate_json()` must return a `Dict[str, Any]` — parse JSON inside the provider, never outside.
- `generate_embedding()` must return a `List[float]`; use `generate_fallback_embedding()` from `engine/utils.py` when the provider cannot embed.
- Default provider: Gemini (`gemini-2.5-flash` + `text-embedding-004`).

### Database
- A single SQLite3 connection per `GameEngine` instance; initialised by `init_db()` in `engine/db/schema.py`.
- `conn.row_factory = sqlite3.Row`; always cast rows to `dict(row)` before returning.
- All SQL goes through `Repository` or `VectorStore`; never issue raw SQL elsewhere.
- `ON DELETE CASCADE` is enforced on all child tables; deleting a campaign cleans everything.
- WAL journal mode and `PRAGMA foreign_keys = ON` are set at connection time — do not disable these.
- Run column-existence migrations in `init_db()` when adding new columns to existing tables (see the `population` migration as a pattern).

### Memory & RAG
- Short-term memory: in-process `dict[campaign_id → list]`, capped at 10 entries, rebuilt from `VectorStore` on restart.
- Long-term memory: `VectorStore` using cosine similarity over stored embeddings (numpy if available, pure Python fallback). Retrieval score = `0.7 * cosine_sim + 0.3 * importance`.
- Periodic summarisation: every `config.SUMMARY_INTERVAL_TURNS` turns (default 10), `CampaignSummarizer` condenses the last N memories into a chapter summary stored in `campaigns.summary`.
- Importance scoring via `calculate_importance()` in `engine/memory/importance.py`; threshold `config.IMPORTANCE_THRESHOLD` (default 0.2) filters low-value memories from RAG retrieval.

### API Endpoints
- All routes are prefixed with `/api/`.
- `POST /api/campaigns` — create campaign (returns first `TurnResponseDTO`).
- `POST /api/turn` — execute a player turn.
- `GET /api/campaigns/{id}/history` — full turn-by-turn world state list.
- `POST /api/campaigns/{id}/rollback` — rewind to a specific turn (deletes later states and memories).
- `GET /api/campaigns/{id}/export` / `POST /api/campaigns/import` — savegame portability.
- `POST /api/campaigns/{id}/estimate_action` — pre-flight cost estimate for a free-text action.
- Raise `HTTPException(status_code=404)` for missing resources; `HTTPException(500)` for unexpected errors, forwarding `str(e)` as `detail`.

### LLM JSON Response Schema
The game master prompt (`GAME_MASTER_SYSTEM_INSTRUCTION` in `state_manager.py`) mandates this exact structure:

```json
{
  "aventura": "<narrative with 3 numbered options at the end>",
  "clima": "aventura | calmo | frenetico | harmonia | desenvolvimento | desespero",
  "opcoes": [
    { "texto": "1. ...", "impacto": { "dinheiro": -500, "poder_militar": 0 } },
    { "texto": "2. ...", "impacto": { "dinheiro": -300, "poder_militar": 200 } },
    { "texto": "3. ...", "impacto": { "dinheiro": null, "poder_militar": null } }
  ],
  "status_reino": {
    "nome_reino": "string", "imperador": "string",
    "dinheiro": 5000, "populacao": 10000,
    "religião": "string", "poder_militar": 1000, "felicidade": "70%"
  }
}
```

- `dinheiro` and `poder_militar` inside `impacto` must be integers or `null` (uncertain outcome).
- `felicidade` is always a string with `%` (e.g. `"75%"`).
- `populacao` is an integer without separators; parse defensively removing `.` and `,` (see `_process_turn_response`).
- Kingdoms always start with `"religião": "Nenhuma"` and the first turn's decision is always the religion choice.

### Narrative Language
- All in-game narrative, variable names in domain models, and JSON field names are **Portuguese** (e.g. `aventura`, `nome_reino`, `poder_militar`, `felicidade`).
- Code comments, docstrings, and API/internal logs may be Portuguese or English.
- Narrative tone is formal and majestic ("Vossa Majestade", "Sua Graça") with no emojis.

### `clima` / Music Mood
Valid values: `aventura`, `calmo`, `frenetico`, `harmonia`, `desenvolvimento`, `desespero`.
`_infer_clima()` in `GameEngine` provides keyword-based fallback inference when the LLM omits or misspells the field.

### Entity Updates (optional LLM extension)
The LLM may include optional top-level keys in its JSON response to update game entities:
- `"personagens"` → `repo.upsert_character()`
- `"quests"` → `repo.upsert_quest()`
- `"itens"` → `repo.upsert_item()`

These are processed in `_process_turn_response()` and are additive — they do not replace existing entities.

## Configuration Reference

| Variable | Default | Purpose |
|---|---|---|
| `DEFAULT_LLM_PROVIDER` | `gemini` | Active provider |
| `RPG_DB_PATH` | `data/rpg_game.db` | SQLite3 file location |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini chat model |
| `GEMINI_EMBEDDING_MODEL` | `text-embedding-004` | Gemini embedding model |
| `GROK_MODEL` | `grok-2-latest` | Grok chat model |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI chat model |
| `OLLAMA_MODEL` | `llama3.2` | Ollama local model |
| `TOP_K_MEMORIES` | `5` | RAG results per turn |
| `IMPORTANCE_THRESHOLD` | `0.2` | Minimum importance for RAG retrieval |
| `SUMMARY_INTERVAL_TURNS` | `10` | Turns between summarisation |
| `WEB_HOST` / `WEB_PORT` | `127.0.0.1` / `8000` | FastAPI bind address |

## Testing

- Tests live in `tests/`; run with `pytest`.
- The test suite covers: API (`test_api.py`), compilation (`test_compilation.py`), DB (`test_db.py`), domain (`test_domain.py`), multi-campaign (`test_multi_campaigns.py`), providers (`test_providers.py`), vector store (`test_vector_store.py`).
- Do not add tests unless explicitly requested.

## Adding a New LLM Provider

1. Create `engine/providers/<name>_provider.py` implementing `BaseLLMProvider`.
2. Register the new provider in `LLMFactory.get_provider()` inside `engine/providers/factory.py`.
3. Add corresponding API key / model config variables to `config.py` and `.env` template.
