# 🔄 System: Turn Execution Lifecycle

## Overview
O ciclo de vida de execução de um turno é o coração operacional do **AI RPG Game**. Ele processa a entrada do jogador, recupera o contexto híbrido, invoca o Game Master e persiste as consequências no mundo determinístico.

---

## Sequência Passo a Passo

```
1. [User Input] -> POST /api/turn (TurnRequestDTO)
       │
       ▼
2. [GameEngine.execute_turn(campaign_id, action)]
       │
       ├─► a. Obter último status do reino (Repository.get_latest_world_state)
       ├─► b. Obter histórico imediato de turnos (Repository.get_history)
       ├─► c. Buscar memórias RAG relevantes (VectorStore.search)
       ├─► d. Recuperar eventos periódicos e tarefas ativas
       ├─► e. Executar arbitragem com ActionEvaluator + FormulaEvaluator (cálculo determinístico de impostos e eventos)
       │
       ▼
3. [ContextBuilder.build_prompt()] -> Monta instrução completa do Game Master (com eventos disparados e projeção)
       │
       ▼
4. [LLMFactory -> FallbackLLMProvider.generate_json(prompt)]
       │
       ▼
5. [GameEngine._process_turn_response()]
       ├─► Sanitização numérica de ouro, população e exército
       ├─► Formatação de felicidade (%) e inferência de clima
       ├─► Upsert em NPCs, Quests ou Itens (se enviados pelo LLM)
       │
       ▼
6. [Persistência]
       ├─► Repository.save_world_state(novo_estado)
       ├─► VectorStore.add_memory(novo_evento, embedding, importancia)
       ├─► CampaignSummarizer.check_and_summarize() (se turno % 10 == 0)
       │
       ▼
7. [Retorno] -> TurnResponseDTO serializado para a interface
```

---

## Tratamento de Falhas e Sanitização

- **Falha de Provedor LLM**: O `FallbackLLMProvider` tenta sequencialmente outros provedores configurados até o `MockFallbackProvider`.
- **Parsing de População**: Remove caracteres separadores (`.` ou `,`) e garante conversão para inteiro seguro.
- **Clima Inválido**: O método `_infer_clima()` analisa a narrativa e seleciona o humor musical mais adequado automaticamente.
