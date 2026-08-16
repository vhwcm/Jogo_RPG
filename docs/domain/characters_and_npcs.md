# 👥 Domain: Characters & NPCs

## Purpose
Modelar e persistir os personagens não-jogáveis (NPCs), ministros, generais, embaixadores e antagonistas com quem o imperador interage ao longo da história.

---

## Schema & Attributes (`characters`)

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `INTEGER PK` | Identificador único do personagem |
| `campaign_id` | `INTEGER FK` | Campanha à qual o personagem pertence |
| `name` | `TEXT` | Nome do personagem |
| `role` | `TEXT` | Cargo/Ocupação (ex: "General do Exército", "Conselheiro Real") |
| `location` | `TEXT` | Localização atual (ex: "Capital Real", "Fronteira Norte") |
| `is_alive` | `INTEGER` | `1` se vivo, `0` se falecido |
| `relationship_with_player` | `TEXT` | Afinidade (ex: "Leal", "Desconfiado", "Hostil", "Aliado") |
| `knowledge_json` | `TEXT` | Fatos, segredos ou informações conhecidas serializadas em JSON |

---

## Business Rules

1. **Descoberta Incremental (Additive Entities)**:
   - Quando o LLM menciona a introdução ou atualização de um personagem no payload JSON (`"personagens"`), o sistema realiza um `upsert` na tabela `characters`.
   - Entidades já existentes são atualizadas com novos dados de afinidade, localização ou conhecimento sem duplicar o registro.
2. **Injeção no Contexto**:
   - Os personagens relevantes presentes no turno atual são injetados pelo `ContextBuilder` no prompt do Game Master para manter consistência de personalidade e relacionamentos.
3. **Cascatas de Exclusão**:
   - Personagens são excluídos automaticamente se a campanha correspondente for deletada.

---

## Related Code
- `engine/db/repository.py`: `upsert_character`, `get_characters`, `get_character_by_name`.
- `engine/domain/state_manager.py`: Processamento de entidades adicionais em `_process_turn_response`.
