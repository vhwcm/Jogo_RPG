# 📜 Domain: Quests & Missions

## Purpose
Gerenciar as missões de estado, demandas diplomáticas, expedições e crises que requerem intervenção contínua do jogador ao longo dos turnos.

---

## Schema & Attributes (`quests`)

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `INTEGER PK` | Identificador único da missão |
| `campaign_id` | `INTEGER FK` | Campanha associada |
| `title` | `TEXT` | Título da missão |
| `description` | `TEXT` | Descrição narrativa detalhada do problema/objetivo |
| `status` | `TEXT` | Estado: `ativa`, `concluida`, `falhou`, `pendente` |
| `objective` | `TEXT` | Critério de conclusão |
| `reward` | `TEXT` | Recompensa estimada em ouro, terras ou alianças |

---

## Business Rules

1. **Ciclo de Vida de Quests**:
   - `Descoberta / Oferta` (`status: ativa`) → `Progresso ao longo dos turnos` → `Conclusão` (`status: concluida`) ou `Falha` (`status: falhou`).
2. **Atualização Dinâmica por IA**:
   - O Game Master pode enviar atualizações de missões no payload JSON (`"quests"`), que são persistidas via `Repository.upsert_quest()`.
3. **Visibilidade no Painel**:
   - A interface web e o resumo de turno exibem missões em andamento para orientar a tomada de decisão do jogador.

---

## Related Code
- `engine/db/repository.py`: `upsert_quest`, `get_active_quests`, `get_all_quests`.
- `engine/domain/state_manager.py`: Integração em `_process_turn_response`.
