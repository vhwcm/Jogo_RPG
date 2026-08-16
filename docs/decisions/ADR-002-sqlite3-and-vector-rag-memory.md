# ADR-002: Persistência SQLite3 com Memória Episódica RAG Híbrida

* **Status**: Aceito
* **Data**: 2026-08-15
* **Decisores**: Equipe de Desenvolvimento AI RPG

## Contexto
Confiar exclusivamente na janela de contexto de modelos de IA gera alucinações sobre números exatos de recursos e custos excessivos em campanhas longas. O jogo requer rastreamento exato do estado do reino e recuperação inteligente de eventos passados.

## Decisão
1. Utilizar **SQLite3** em modo WAL e foreign keys ativas para armazenar tabelas estruturadas (`campaigns`, `world_state`, `characters`, `quests`, `items`, `memories`).
2. Implementar busca por vetores de semântica (Cosine Similarity em Python/NumPy) combinada com cálculo determinístico de importância (`0.7 * cos_sim + 0.3 * importance`).

## Alternativas Consideradas
- **PostgreSQL + pgvector**: Excelente para alta escala, mas exige instalação de servidor externo e quebra a facilidade de instalação zero-dependency do projeto.
- **ChromaDB / Pinecone**: Dependências externas pesadas ou serviços em nuvem pagos desnecessários para a escala local de campanhas.

## Consequências
- **Positivas**:
  - Instalação 100% autônoma e local.
  - Baixo consumo de memória e tokens.
  - Integridade relacional estrita com `ON DELETE CASCADE`.
- **Negativas**:
  - Busca vetorial sem índice HNSW nativo, porém com performance instantânea (<5ms) para os milhares de turnos de uma campanha individual.
