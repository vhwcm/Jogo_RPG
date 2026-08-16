# 🧪 Módulo Tests (`tests`)

O módulo `tests` contém a suíte completa de testes automatizados do sistema, garantindo a integridade da lógica de domínio, persistência em banco de dados, busca vetorial, endpoints da API e isolamento de provedores de IA.

---

## 📂 Arquivos de Teste

| Arquivo | Escopo dos Testes |
|---|---|
| **`test_domain.py`** | Validação dos modelos `@dataclass`, parsing de respostas do turno e integridade do `KingdomStatus`. |
| **`test_actions.py`** | Testes do protocolo de `GameAction` (criação e remoção de estruturas/itens, atualização de progresso de tarefas e mutações diplomáticas). |
| **`test_db.py`** | Testes de inicialização de schema SQLite, integridade referencial, foreign keys e operações CRUD do `Repository`. |
| **`test_vector_store.py`** | Testes de cálculo de similaridade de cosseno, filtros de importância e recuperação de memórias RAG. |
| **`test_providers.py`** | Testes unitários dos adaptadores de LLM (`Gemini`, `Grok`, `OpenAI`, `Ollama`) utilizando mocks para evitar consumo de créditos de API. |
| **`test_api.py`** | Testes de integração dos endpoints FastAPI usando `fastapi.testclient.TestClient`. |
| **`test_multi_campaigns.py`** | Testes de concorrência e isolamento rigoroso de dados entre múltiplas campanhas no mesmo banco. |
| **`test_compilation.py`** | Verificação estática de sintaxe e importação de todos os módulos Python do repositório. |

---

## 🚀 Como Executar os Testes

Execute todos os testes com saída detalhada:
```bash
pytest -v
```

Para executar um arquivo de teste específico:
```bash
pytest tests/test_actions.py -v
```
