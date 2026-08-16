# 💾 System: Campaign Import & Export (Savegame Portability)

## Overview
O sistema permite exportar o estado integral de qualquer campanha para um arquivo JSON portátil e restaurá-lo em qualquer outra instalação ou máquina.

---

## Formato do Savegame JSON

```json
{
  "version": 1,
  "exported_at": "2026-08-16T12:00:00Z",
  "campaign": {
    "name": "Império Solar",
    "summary": "Crônicas do reinado...",
    "created_at": "...",
    "updated_at": "..."
  },
  "world_states": [
    {
      "turn_number": 1,
      "kingdom_name": "Solaria",
      "ruler_name": "Aurelius",
      "race": "humano",
      "gold": 5000,
      "population": 10000,
      "religion": "Fé da Luz",
      "military": 1000,
      "happiness": "70%"
    }
  ],
  "characters": [...],
  "quests": [...],
  "items": [...],
  "memories": [...]
}
```

---

## Fluxo de Importação (`engine/domain/state_manager.py`)

1. **Validação de Payload**: Valida compatibilidade de versão e campos essenciais (`name`, `world_states`).
2. **Transação Atômica**:
   - Cria nova campanha com novo ID único.
   - Insere todos os registros de `world_state`, `characters`, `quests` e `memories` vinculados ao novo ID.
3. **Reconstrução de Cache**:
   - Reconstrói a memória de curto prazo em memória para a nova campanha importada.
4. **Retorno**: Devolve os dados da campanha importada pronta para jogo imediato.
