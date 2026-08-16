# 🧠 Domain: Memory & RAG Layer

## Purpose
Garantir retenção contínua de contexto, memórias de longo prazo e coerência narrativa em campanhas de qualquer extensão, mantendo o consumo de tokens sob controle.

---

## As 4 Camadas de Memória

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Memória de Curto Prazo (Short-Term Window)               │
│    - Últimos 4 a 10 turnos em memória de processo/banco     │
├─────────────────────────────────────────────────────────────┤
│ 2. Estado Estruturado Determinístico                        │
│    - Valores exatos de ouro, população, exército, felicidade│
├─────────────────────────────────────────────────────────────┤
│ 3. Memória Episódica RAG (Vector Store)                     │
│    - Busca por similaridade de cosseno + importância        │
├─────────────────────────────────────────────────────────────┤
│ 4. Resumo Hierárquico de Capítulos                          │
│    - Compressão periódica a cada N turnos (default 10)      │
└─────────────────────────────────────────────────────────────┘
```

---

## Algoritmo de Ranqueamento RAG

O `VectorStore` calcula a pontuação final de cada memória usando uma média ponderada entre a similaridade de cosseno do embedding vetorial e a importância intrínseca do evento:

$$\text{Score} = (0.7 \times \text{CosineSimilarity}) + (0.3 \times \text{Importance})$$

### Pontuação de Importância (`engine/memory/importance.py`):
- Avalia palavras-chave de alto impacto dramático (ex: "guerra", "morte", "aliança", "traição", "ouro", "coroação", "catástrofe").
- Retorna um float entre `0.0` e `1.0`.
- Memórias abaixo de `IMPORTANCE_THRESHOLD` (padrão: `0.2`) são descartadas da recuperação RAG para não poluir o prompt.

---

## Assembly de Prompt (`ContextBuilder`)

O `ContextBuilder` reúne as 4 camadas em uma instrução limpa e estruturada:
1. **História Preexistente**: `campaigns.summary`.
2. **Estado Atual**: Nome do Reino, Imperador, Ouro, População, Exército, Felicidade, Religião.
3. **Memórias Relevantes Recuperadas**: Top-K eventos episódicos mais pertinentes à ação atual.
4. **NPCs & Missões Ativas**: Personagens conhecidos na localidade e objetivos em aberto.
5. **Diálogo Imediato**: Últimas interações do jogador e respostas do Game Master.

---

## Related Code
- `engine/memory/context_builder.py`: Montagem completa do prompt.
- `engine/memory/importance.py`: `calculate_importance()`.
- `engine/db/vector_store.py`: Armazenamento e busca vetorial com fallback NumPy/Python.
