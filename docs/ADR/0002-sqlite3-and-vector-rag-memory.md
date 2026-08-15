# ADR 0002: Armazenamento SQLite3 e Memória Episódica RAG

* **Status**: Aceito
* **Data**: 2026-08-15
* **Autor**: Antigravity AI & Usuário

## 📋 Contexto

Confiar apenas no histórico corrido do prompt do LLM causa alucinações sobre números exatos (dinheiro, lealdade de NPCs) e gera custos exorbitantes em campanhas longas. O RPG necessita de um estado determinístico para recursos e de uma recuperação semântica para acontecimentos passados.

## 🎯 Decisão

1. Usar **SQLite3** como banco de dados único e sem dependências externas complexas para salvar:
   - Tabelas estruturadas de estado (`campaigns`, `world_state`, `characters`, `quests`, `items`).
   - Tabela de memórias episódicas (`memories`) onde cada registro salva o evento, o turno, os envolvidos e o vetor embedding (JSON/Blob).
2. Implementar busca por vetores de semântica (**Cosine Similarity em Python/NumPy**) combinada com pontuação de importância (*importance score*) e filtros relacionais (ex: busca por memórias do personagem 'Marcus').

## ⚡ Consequências

- **Positivas**:
  - Zero necessidade de subir containers de bancos de dados adicionais (como PostgreSQL/pgvector ou Pinecone).
  - Execução 100% local, portátil e resiliente em qualquer máquina.
  - Consumo de tokens drasticamente reduzido (apenas as 5 memórias mais relevantes são enviadas ao LLM).
- **Negativas**:
  - Para bases com milhões de registros vetoriais, a busca por produto escalar em Python puro é menos eficiente que `sqlite-vec` ou C-extensions, mas atende perfeitamente ao escopo do RPG.
