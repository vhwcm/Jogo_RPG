# 🗄️ Submódulo Database (`engine/db`)

O submódulo `engine/db` é responsável pela camada de persistência de dados do jogo. Ele gerencia o banco relacional SQLite3 com suporte a WAL mode e busca vetorial de similaridade por cosseno para o mecanismo de RAG (Retrieval-Augmented Generation).

---

## 📂 Arquivos do Módulo

- **`schema.py`**: Definição DDL das tabelas e migrações do banco SQLite, além do método `init_db()`.
- **`repository.py`**: Implementação do padrão Repository (CRUD) para acesso às entidades relacionais e estados de turno.
- **`vector_store.py`**: Gerenciador de memórias episódicas e busca semântica por embeddings via similaridade de cosseno.

---

## 📊 Estrutura das Tabelas

| Tabela | Descrição |
|---|---|
| `campaigns` | Cadastro principal de campanhas com nome, data de criação e resumo acumulado. |
| `world_state` | Histórico turno a turno dos recursos (ouro, população, poder militar, felicidade, religião e estado bruto). |
| `characters` | Personagens e NPCs com função, localização, lealdade e conhecimento em JSON. |
| `quests` | Missões ativas, completadas ou falhas com objetivos e descrições. |
| `memories` | Eventos episódicos com texto narrativo, nível de importância (0.0 a 1.0) e vetor de embedding serializado. |
| `campaign_items` | Patrimônio do reino: construções, estruturas, postos avançados, santuários, artefatos, itens e criaturas. |
| `campaign_tasks` | Projetos de longo prazo, tarefas ativas e incidentes dinâmicos com progresso percentual (0 a 100%). |
| `campaign_allies` | Relações diplomáticas com outros impérios, incluindo poder militar, população, relacionamento (-100 a +100) e status. |

---

## 🔍 Busca Vetorial (RAG)

O `VectorStore` armazena os embeddings gerados pelos provedores de IA em formato JSON e implementa a fórmula matemática do cosseno para ordenar as memórias mais relevantes:

$$\text{Similaridade} = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$

As memórias com maior pontuação de similaridade e relevância acima do limiar mínimo são injetadas no contexto do próximo turno.
