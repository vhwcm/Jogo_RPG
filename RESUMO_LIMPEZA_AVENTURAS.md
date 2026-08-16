# Resumo: Limpeza de Campanhas e Aventuras de Teste

## Objetivo
Remover todas as campanhas, aventuras e dados de teste acumulados no banco de dados SQLite (`data/rpg_game.db`), deixando o ambiente limpo para novas aventuras.

## Ações Executadas
1. **Inspeção Prévia**:
   - Identificadas 104 campanhas de teste e suas respectivas entidades vinculadas (`world_state`, `memories`, `campaign_items`, `campaign_tasks`, `campaign_map_nodes`, `campaign_map_edges`).
2. **Exclusão com Cascade**:
   - Ativada a integridade referencial (`PRAGMA foreign_keys = ON;`).
   - Executada a exclusão total da tabela `campaigns` (`DELETE FROM campaigns;`), propagando a remoção para todas as tabelas dependentes via `ON DELETE CASCADE`.
3. **Otimização de Espaço (VACUUM)**:
   - Executado o comando `VACUUM` no SQLite para desfragmentar o banco e liberar espaço em disco.
4. **Verificação de Estado Final**:
   - Todas as tabelas relacionais do banco de dados agora possuem contagem `0`:
     - `campaigns`: 0
     - `world_state`: 0
     - `characters`: 0
     - `quests`: 0
     - `items`: 0
     - `locations`: 0
     - `memories`: 0
     - `campaign_items`: 0
     - `campaign_tasks`: 0
     - `campaign_allies`: 0
     - `campaign_map_nodes`: 0
     - `campaign_map_edges`: 0
     - `periodic_events`: 0
