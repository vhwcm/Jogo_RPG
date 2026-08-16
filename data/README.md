# 💾 Módulo Data (`data`)

O diretório `data` é o local de armazenamento persistente para o banco de dados principal do jogo (**SQLite3**).

---

## 📂 Arquivos Armazenados

- **`rpg_game.db`**: Arquivo principal do banco de dados SQLite contendo todas as tabelas relacionais (`campaigns`, `world_state`, `characters`, `quests`, `memories`, `campaign_items`, `campaign_tasks`, `campaign_allies`).
- **`rpg_game.db-wal`** & **`rpg_game.db-shm`**: Arquivos auxiliares gerados automaticamente pelo mecanismo de concorrência **WAL (Write-Ahead Logging)** do SQLite, garantindo alta performance de leitura e gravação assíncrona.

---

## 🔒 Boas Práticas e Manutenção

1. **Backups**: Para fazer backup de uma campanha, utilize o endpoint de exportação `/api/campaigns/{id}/export` ou copie o arquivo `rpg_game.db` quando o servidor estiver inativo.
2. **Exclusão de Dados**: Para resetar completamente o estado do banco e começar do zero, basta remover o arquivo `rpg_game.db`. O sistema recria o schema automaticamente na próxima inicialização via `init_db()`.
3. **Controle de Versão**: Os arquivos `.db`, `.db-shm` e `.db-wal` são ignorados no controle de versão Git (`.gitignore`) para preservar os dados locais de cada ambiente.
