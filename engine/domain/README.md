# 👑 Submódulo Domain (`engine/domain`)

O submódulo `engine/domain` concentra os modelos de domínio e a máquina de estados central (`GameEngine`) que rege as regras de negócio e a progressão narrativa do RPG.

---

## 📂 Arquivos do Módulo

- **`models.py`**: Modelos de dados fortemente tipados utilizando `@dataclass` para representar todas as entidades do jogo.
- **`state_manager.py`**: O coração operacional da engine (`GameEngine`), responsável pela orquestração do loop de turnos, execução de mutações atômicas no mundo, prompts do Game Master e integração entre banco, memória e IA.

---

## 🧩 Modelos de Domínio (`models.py`)

- **`KingdomStatus`**: Guarda os dados vitais do reino (nome, soberano, ouro, população, religião, exército, felicidade).
- **`Item`**: Representa qualquer patrimônio material, estrutura, fortificação, santuário, monumento, recurso ou criatura do reino.
- **`Task`**: Tarefas e incidentes com título, status (`em_andamento`, `concluida`, `falha`), percentual de progresso e duração estimada.
- **`ImperioAliado`**: Entidades geopolíticas externas com nome do soberano, população, poderio militar, afinidade (-100 a 100) e status diplomático.
- **`GameAction`**: Ação atômica emitida pela IA para alterar o estado do mundo (`action_type` e `payload`).
- **`TurnResponse`**: Resposta consolidada de um turno (texto épico, status do reino, clima narrativo, 3 opções numeradas e lista de ações executadas).

---

## ⚙️ Gerenciador de Estado (`GameEngine` em `state_manager.py`)

### Responsabilidades:
1. **`create_campaign()`**: Cria nova campanha, inicializa o estado de turno 1 e aciona a IA para narrar a introdução do reino.
2. **`process_turn()`**:
   - Monta o contexto com o `ContextBuilder` (RAG, histórico e estado).
   - Envia o prompt estruturado com exigência de retorno JSON para a IA.
   - Higieniza e valida o JSON de resposta com `utils.py`.
   - Executa as `GameAction` (criação/remoção de patrimônio, atualização de tarefas e diplomacia).
   - Salva o novo estado estruturado em `world_state` e o evento no `VectorStore`.
3. **`estimate_action_impact()`**: Permite que a IA antecipe previsões de impacto (ouro, tropas, população) para uma ação hipotética do jogador.
4. **`rollback_turn()`**: Reverte o jogo para um turno anterior, expurgando estados subsequentes e restaurando a integridade histórica.
