# 🧪 Guide: Testing & Quality Assurance

## 1. Filosofia de Testes
O projeto prioriza testes rápidos, determinísticos e sem dependências externas de rede durante a execução em CI/CD. Chamadas reais a APIs de LLM são substituídas por mocks determinísticos nos testes unitários.

---

## 2. Estrutura da Suíte de Testes (`tests/`)

- `test_db.py`: Validação de DDL SQLite, foreign keys, constraints e operações CRUD no `Repository`.
- `test_vector_store.py`: Validação de cálculo de similaridade de cosseno, limiar de importância e ordenação de memórias.
- `test_domain.py`: Testes da `GameEngine`, fluxo de criação de campanhas, rollbacks e isolamento entre partidas.
- `test_providers.py`: Testes de inicialização, parsing de JSON e cadeia de fallback dos provedores.
- `test_api.py`: Testes de integração dos endpoints FastAPI (`TestClient`) validando DTOs de entrada e saída.

---

## 3. Executando os Testes

```bash
# Executar toda a suíte de testes
pytest

# Executar com relatório verboso
pytest -v

# Executar arquivo específico
pytest tests/test_domain.py
```

---

## 4. Diretrizes para Novos Testes
- Nunca inclua comentários no código dos testes.
- Utilize nomes de métodos autoexplicativos que descrevam o cenário e o resultado esperado (ex: `test_rollback_prunes_memories_after_target_turn`).
- Garanta que qualquer alteração de regra de negócio seja acompanhada de um teste que falhe antes da correção (TDD).
