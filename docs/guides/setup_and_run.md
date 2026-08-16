# 🚀 Guide: Setup & Execution

## 1. Pré-requisitos
- Python 3.10 ou superior.
- Virtualenv (`python3 -m venv`).
- Chave de API de pelo menos um provedor suportado (Google Gemini, xAI Grok, OpenAI) ou uma instância do Ollama local em execução.

---

## 2. Instalação Passo a Passo

```bash
# 1. Clonar o repositório e entrar no diretório
cd /home/exati/AI_RPG_GAME

# 2. Executar script de instalação automática
./install.sh

# Ou configurar manualmente o virtual environment:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Configuração do `.env`

Crie ou edite o arquivo `.env` na raiz do projeto:

```env
DEFAULT_LLM_PROVIDER=gemini
GEMINI_API_KEY=sua_chave_gemini_aqui
GEMINI_MODEL=gemini-2.5-flash

# Opcionais para redundância / fallback
GROK_API_KEY=sua_chave_grok_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 4. Diagnóstico de Conectividade

Antes de iniciar uma partida, valide a conectividade das suas APIs:

```bash
python3 check_api.py
```

---

## 5. Execução do Jogo

```bash
# Iniciar o Servidor FastAPI e abrir a Interface Web
python3 run.py

# Ou iniciar diretamente em segundo plano / terminal
uvicorn server.app:app --host 127.0.0.1 --port 8000 --reload
```

Acesse a interface em `http://127.0.0.1:8000`.
