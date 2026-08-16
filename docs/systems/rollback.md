# ⏪ System: Turn Rollback Mechanism

## Overview
O mecanismo de rollback permite ao jogador voltar no tempo para qualquer turno anterior de uma campanha, desfazendo decisões desastrosas e explorando linhas temporais alternativas.

---

## Fluxo de Execução do Rollback

```
1. [User Input] -> POST /api/campaigns/{id}/rollback { "target_turn": 5 }
       │
       ▼
2. [GameEngine.rollback(campaign_id, target_turn)]
       │
       ├─► a. Valida se target_turn existe no histórico
       ├─► b. Deleta registros de world_state com turn_number > target_turn
       ├─► c. Deleta memórias episódicas com turn_number > target_turn
       ├─► d. Limpa e reconstrói a janela de memória de curto prazo
       │
       ▼
3. [Recupera Status do Turno Restaurado]
       │
       ▼
4. [Retorno] -> TurnResponseDTO com o estado exato restaurado
```

---

## Garantias de Consistência
- **Integridade de Memórias**: Todas as memórias geradas em turnos posteriores ao `target_turn` são removidas do `VectorStore` para evitar que a IA se lembre de "futuros que foram apagados".
- **Estado Determinístico**: Os recursos do reino voltam exatamente ao valor salvo no `world_state` do turno destino.
