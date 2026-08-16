# Resumo de Correção: Isolamento do `campaign_id` no SQLite e Vínculo de Novas Aventuras na UI

## 1. Causa Raiz Identificada
Ao criar uma nova aventura no sistema, o evento de recolhimento de impostos não era exibido na interface por conta de duas causas cruzadas:

1. **Conflito de ID Global no SQLite (`periodic_events`)**:
   - A tabela `periodic_events` utiliza `id TEXT PRIMARY KEY`.
   - Ao registrar o evento inicial de impostos com o ID fixo `"recolhimento_impostos"`, o comando `ON CONFLICT(id) DO UPDATE SET` colidia com a chave primária de campanhas anteriores no banco de dados e não atualizava o campo `campaign_id`.
   - Consequentemente, o evento permanecia associado à primeira campanha criada. Quando uma segunda aventura fazia a consulta `SELECT * FROM periodic_events WHERE campaign_id = 'camp_2'`, a busca retornava uma lista vazia (`[]`).

2. **Desvinculação do `campaign_id` no Frontend Web**:
   - Ao criar uma nova campanha via `POST /api/campaigns`, a API não serializava o `campaign_id` no DTO retornado (`TurnResponseDTO`).
   - O código do frontend (`web/js/app.js`) fazia um `fetch('/api/campaigns')` e selecionava cegamente `camps[0].id` (a campanha mais antiga), fazendo com que a UI exibisse os eventos e o estado de outra aventura anterior do usuário.

---

## 2. Solução Implementada

1. **Isolamento de IDs de Eventos por Campanha**:
   - Em `engine/domain/state_manager.py`, a criação de campanhas passa a gerar IDs de eventos periódicos únicos vinculados ao `campaign_id` (ex: `f"recolhimento_impostos_{campaign_id}"`).
   - Em `engine/db/repository.py`, a instrução `ON CONFLICT(id) DO UPDATE SET` foi atualizada para incluir `campaign_id = excluded.campaign_id`.

2. **Inclusão do `campaign_id` nos DTOs de Resposta**:
   - Em `server/dto.py` e `engine/domain/models.py`, adicionado o campo `campaign_id` na classe `TurnResponseDTO` / `TurnResponse`.
   - Em `server/app.py`, os endpoints de criação de campanha (`POST /api/campaigns`) e execução de turno (`POST /api/turn`) passaram a retornar explicitamente o `campaign_id`.

3. **Atualização da Seleção de Campanha Ativa na UI**:
   - Em `web/js/app.js`, a criação de uma nova aventura utiliza diretamente `data.campaign_id` para definir `currentCampaignId` e executa imediatamente `refreshStateDetails(currentCampaignId)`, garantindo que a interface recarregue os eventos da nova campanha.

---

## 3. Resultados dos Testes
- **pytest**: 67 de 67 testes unitários e de API aprovados com 100% de sucesso.
- **Validação de API**: O teste `test_api_campaign_creation_and_turn` confirma que `POST /api/campaigns` retorna `campaign_id` e que `GET /api/campaigns/{campaign_id}/state-details` retorna o evento de recolhimento de impostos ativo no dia 30.
