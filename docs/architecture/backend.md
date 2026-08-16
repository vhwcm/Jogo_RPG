# ⚙️ Backend Architecture (FastAPI & Engine)

## 1. Módulo Server (`server/`)

O módulo `server/` expõe a API RESTful do jogo através do framework FastAPI.

### Responsabilidades:
- Validação e tipagem de requisições e respostas via Pydantic DTOs (`server/dto.py`).
- Roteamento e tratamento de exceções HTTP (`server/app.py`).
- Servir arquivos estáticos da interface web (`web/`).
- Gestão do ciclo de vida da instância de `GameEngine` através de injeção de dependência.

### Endpoints REST Principais:

| Método | Rota | Descrição | DTO de Entrada | DTO de Saída |
|---|---|---|---|---|
| `GET` | `/api/status` | Healthcheck e provedor LLM ativo | - | `StatusDTO` |
| `POST` | `/api/campaigns` | Cria nova campanha e executa o turno 1 | `CreateCampaignDTO` | `TurnResponseDTO` |
| `GET` | `/api/campaigns` | Lista todas as campanhas | - | `List[CampaignSummaryDTO]` |
| `GET` | `/api/campaigns/{id}` | Recupera status da campanha ativa | - | `CampaignStatusDTO` |
| `POST` | `/api/turn` | Processa a ação/decisão do turno atual | `TurnRequestDTO` | `TurnResponseDTO` |
| `GET` | `/api/campaigns/{id}/history` | Histórico de todos os turnos da campanha | - | `List[WorldStateDTO]` |
| `POST` | `/api/campaigns/{id}/rollback` | Reverte a campanha para um turno anterior | `RollbackRequestDTO` | `TurnResponseDTO` |
| `GET` | `/api/campaigns/{id}/export` | Exporta savegame completo em JSON | - | `SavegameExportDTO` |
| `POST` | `/api/campaigns/import` | Importa savegame a partir de JSON | `SavegameImportDTO` | `CampaignSummaryDTO` |
| `POST` | `/api/campaigns/{id}/estimate_action` | Estima impacto e custo de ação livre | `EstimateActionDTO` | `ActionEstimateDTO` |

---

## 2. Orquestração de Domínio (`engine/domain/state_manager.py`)

A classe `GameEngine` atua como a fachada do domínio e coordenadora central:

```python
class GameEngine:
    def __init__(self, db_path: str = None, default_provider: str = None):
        self.conn = get_connection(db_path)
        self.repo = Repository(self.conn)
        self.vector_store = VectorStore(self.conn)
        self.context_builder = ContextBuilder(self.repo, self.vector_store)
        self.summarizer = CampaignSummarizer(self.repo, self.provider)
```

### Principais Métodos:
- `create_campaign(name, race, ruler_name, kingdom_name)`: Inicializa campanha, estado inicial do reino e dispara a narrativa inicial.
- `execute_turn(campaign_id, player_action)`: Orquestra o ciclo completo de um turno.
- `rollback(campaign_id, target_turn)`: Trunca estados posteriores ao turno selecionado e reconstrói memórias de curto prazo.
- `export_campaign(campaign_id)` / `import_campaign(data)`: Serialização e deserialização portátil de campanhas.

---

## 3. Gestão de Erros e Exceções

- Entidades não encontradas disparam `HTTPException(status_code=404, detail="...")`.
- Erros de parsing ou inferência do LLM causam ativação de fallback transparente antes de qualquer erro 500.
- Falhas críticas retornam `HTTPException(status_code=500, detail=str(e))` com detalhes estruturados.
