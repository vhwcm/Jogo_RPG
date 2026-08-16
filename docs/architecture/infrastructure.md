# 🏗️ Infrastructure & Configuration

## 1. Gestão de Configuração (`config.py`)

Todas as variáveis de ambiente e parâmetros de infraestrutura são centralizados em `config.py` utilizando `python-dotenv`.

### Parâmetros Suportados:

| Variável de Ambiente | Valor Padrão | Finalidade |
|---|---|---|
| `DEFAULT_LLM_PROVIDER` | `gemini` | Provedor de IA prioritário (`gemini`, `grok`, `openai`, `ollama`, `mock`) |
| `RPG_DB_PATH` | `data/rpg_game.db` | Caminho do arquivo SQLite3 |
| `GEMINI_API_KEY` | - | Chave de API Google Gemini |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Modelo de chat Gemini |
| `GEMINI_EMBEDDING_MODEL` | `text-embedding-004` | Modelo de embedding vetorial |
| `GROK_API_KEY` | - | Chave de API xAI Grok |
| `GROK_MODEL` | `grok-2-latest` | Modelo de chat Grok |
| `OPENAI_API_KEY` | - | Chave de API OpenAI |
| `OPENAI_MODEL` | `gpt-4o-mini` | Modelo de chat OpenAI |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Endpoint do serviço Ollama local |
| `OLLAMA_MODEL` | `llama3.2` | Modelo Ollama |
| `TOP_K_MEMORIES` | `5` | Quantidade de memórias RAG por turno |
| `IMPORTANCE_THRESHOLD` | `0.2` | Limiar mínimo de relevância para inclusão no prompt |
| `SUMMARY_INTERVAL_TURNS` | `10` | Intervalo de turnos para compressão de capítulos |
| `WEB_HOST` | `127.0.0.1` | Host de bind do servidor FastAPI |
| `WEB_PORT` | `8000` | Porta do servidor |

---

## 2. Scripts de Execução e Diagnóstico

- `run.py`: Ponto de entrada unificado para inicialização do servidor FastAPI (`uvicorn`) e abertura opcional da interface web no navegador.
- `install.sh`: Script de criação do virtual environment (`.venv`) e instalação de dependências via `pip`.
- `check_api.py`: Script de diagnóstico para testar conectividade e credenciais com todos os provedores LLM configurados.
- `check_env.sh`: Validação rápida de dependências do sistema e variáveis de ambiente.

---

## 3. Logs & Observabilidade
- O servidor FastAPI utiliza o logger padrão do Python configurado em nível `INFO`.
- As trocas de provedor por fallback em tempo de execução são registradas como alertas informativos no console.
