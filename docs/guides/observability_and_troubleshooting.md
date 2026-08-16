# Guia de Observabilidade, Logs Estruturados e Troubleshooting

Este documento estabelece os padrões e práticas de observabilidade, logging estruturado e fluxo de troubleshooting para o projeto **AI RPG Game**.

---

## 1. Padrões de Logging Estruturado

### Princípios Gerais
- Toda operação relevante deve produzir logs semânticos que contextualizem o estado antes, durante e após sua execução.
- O formato deve permitir correlacionar requisições, turnos e campanhas (`campaign_id`, `turn_number`, `action`, `status`).

### Níveis de Log e Quando Usar

| Nível | Finalidade | Exemplos |
|---|---|---|
| `DEBUG` | Detalhes internos de execução, cálculos intermediários, diagnósticos minuciosos. | Payload sanitizado retornado por LLM, tempo de embedding vetorial. |
| `INFO` | Marcos normais de ciclo de vida e transições de estado bem-sucedidas. | Criação de campanha, execução de turno concluída, avanço de capítulo. |
| `WARNING` | Anomalias recuperáveis ou uso de fallbacks sem quebra de fluxo. | LLM primário expirou timeout, acionando provedor secundário de fallback. |
| `ERROR` | Falha em operação que interrompeu o fluxo normal da requisição. | Exceção ao persistir no SQLite, payload inválido do LLM após retentativas. |
| `CRITICAL` | Falha grave que impede a operação continuada do subsistema. | Corrupção de arquivo de banco de dados, falha irrecuperável de inicialização. |

### Contexto Mínimo Obrigatório nos Logs
Ao emitir logs de operações, inclua metadados estruturados:
- `campaign_id`: ID da campanha ativa.
- `turn_number`: Número do turno em execução.
- `action_type`: Tipo da ação executada (ex: `action_choice`, `free_text`, `tax_adjustment`).
- `provider`: Provedor de IA em uso (ex: `gemini`, `groq`, `openrouter`, `ollama`).
- `duration_ms`: Tempo total de processamento em milissegundos.
- `error_type`: Classe da exceção capturada (em caso de erros).

### Segurança e Sanitização Rigorosa (Zero Secrets)
- **Proibição Absoluta**: NUNCA registre nos logs chaves de API (`GEMINI_API_KEY`, `GROQ_API_KEY`, etc.), credenciais, senhas ou tokens.
- **Sanitização de Headers**: Cabeçalhos HTTP de autorização (`Authorization`, `Bearer ...`) devem ser omitidos ou mascarados.

---

## 2. Fluxo de Troubleshooting para Agentes

Quando um erro ou comportamento anômalo for reportado:

```
                  Identificação do Problema
                             │
                             ▼
               Consultar Logs de Execução
        (Localizar campaign_id, turn, timestamp)
                             │
                             ▼
                 Identificar Causa Raiz
       (Traceback, falha de schema, timeout de LLM)
                             │
                             ▼
         Consultar Procedimentos Conhecidos (Abaixo)
                             │
                             ▼
            Implementar Correção & Teste (TDD)
                             │
                             ▼
       Documentar Novo Procedimento (Se Recorrente)
```

1. **Evidência Antes de Suposição**: O agente deve consultar o log da operação correspondente antes de especular a causa do bug.
2. **Isolamento por Identificador**: Filtrar os logs pelo `campaign_id` ou `turn_number` afetado para isolar a linha do tempo do evento.
3. **Validação de Fallbacks**: Verificar se houve alerta de fallback (`WARNING`) antes da falha final (`ERROR`).

---

## 3. Catálogo de Procedimentos de Troubleshooting Recorrentes

### Procedimento A: Falha na Resposta JSON Estruturada do LLM
- **Sintoma**: Log indica `JSONDecodeError` ou campo obrigatório ausente em `GameEngine.execute_turn()`.
- **Diagnóstico**: Inspecionar log de nível `DEBUG` com a resposta bruta sanitizada do LLM.
- **Resolução**:
  1. Verificar se o prompt inclui o schema JSON esperado com exemplos explícitos.
  2. Testar o provedor com `python check_api.py`.
  3. Acionar fallback para provedor com maior capacidade de raciocínio se o modelo local falhar.

### Procedimento B: Inconsistência de Integridade no SQLite
- **Sintoma**: `sqlite3.IntegrityError: FOREIGN KEY constraint failed`.
- **Diagnóstico**: Inspecionar log de `engine/db/repository.py` verificando a sequência de inserção/deleção.
- **Resolução**:
  1. Verificar se `PRAGMA foreign_keys = ON` está ativo na conexão.
  2. Confirmar se a deleção ou rollback cascateou todas as tabelas filhas de `campaigns`.
  3. Executar `pytest tests/test_db.py` para isolar a query causadora.

### Procedimento C: Timeout ou Rate Limit de Provedor de IA
- **Sintoma**: `HTTPStatusError 429` ou `TimeoutException`.
- **Diagnóstico**: Inspecionar log `WARNING` de `LLMFactory` indicando exaustão de cota no provedor ativo.
- **Resolução**:
  1. Garantir que a lista de provedores em `config.py` possua alternativas configuradas na ordem de prioridade.
  2. Validar que o mecanismo de fallback automático em `LLMFactory` tentou o próximo provedor.
