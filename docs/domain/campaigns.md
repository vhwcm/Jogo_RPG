# 👑 Domain: Campaigns

## Purpose
A entidade `Campaign` representa uma jornada completa de jogo e atua como o agregado raiz (Root Aggregate) para todo o estado de um reino, histórico de turnos, personagens conhecidos, missões ativas e memórias episódicas.

---

## Entities & Models (`engine/domain/models.py`)

```python
@dataclass
class CampaignInfo:
    id: int
    name: str
    summary: str
    created_at: str
    updated_at: str
```

---

## Business Rules

1. **Isolamento de Campanhas**: Todos os dados de turnos, NPCs, quests e memórias possuem uma chave estrangeira estrita (`campaign_id`). O estado de uma campanha nunca vaza para outra.
2. **Criação Inicial (Turno 1)**:
   - Toda campanha começa no Turno 1 com religião definida inicialmente como `"Nenhuma"`.
   - A primeira decisão apresentada ao jogador consiste na escolha do patrono/religião do reino.
3. **Ciclo de Vida**:
   - `Criação` → `Execução de Turnos` → `Rollback (opcional)` → `Exportação/Importação` → `Exclusão (com Cascade)`.
4. **Resumo Acumulado (`summary`)**:
   - A cada ciclo de turnos configurado (padrão: 10), o `CampaignSummarizer` condensa a narrativa anterior e persiste o resumo textual no registro da campanha.

---

## Related Code
- `engine/domain/state_manager.py`: `GameEngine.create_campaign`, `list_campaigns`, `get_campaign`.
- `engine/db/repository.py`: `Repository.create_campaign`, `get_campaign`, `delete_campaign`.
- `server/dto.py`: `CreateCampaignDTO`, `CampaignSummaryDTO`, `CampaignStatusDTO`.
