# 🏰 AI RPG Game - Layered Architecture & Modular Engine

RPG de Estratégia e Narrativa Medieval alimentado por Inteligência Artificial (LLMs), RAG com Vetores e Armazenamento Estruturado em **SQLite3**.

## 🌟 Principais Recursos

- **Arquitetura em Camadas (Clean Architecture)**: Código do motor de jogo (`engine/`) desacoplado e servido via API REST FastAPI.
- **Memória RAG Episódica & Vetorial**: Armazenamento episódico de eventos em SQLite3 com cálculo de *importance score* (0.0 a 1.0) e busca por semântica (cosine similarity) + filtros por personagem e recência.
- **Estado do Mundo Estruturado**: Tabelas relacionais em SQLite3 para reinos, status de recursos, lealdade de NPCs, quests em andamento e itens.
- **Provedores de LLM Plugáveis com Fallback**:
  - 🤖 **Google Gemini** (SDK `google-genai` com `gemini-2.5-flash` e embeddings `text-embedding-004`)
  - ⚡ **xAI Grok API** (`grok-2`)
  - 🟢 **OpenAI** (`gpt-4o-mini`)
  - 🦙 **Ollama (Local / Offline)** (`llama3.2`)
- **Interface Web Moderna**:
  - **Web Application em Glassmorphism** (FastAPI backend + HTML5/CSS3/JS, trilha sonora adaptativa, mapa tático de nós e gerenciamento de inventário/diplomacia)
- **Bateria de Testes Automáticos**: Testes unitários e de integração com `pytest`.
- **Script Diagnóstico de APIs**: `python3 run.py check` para testar conectividade e latência de todas as chaves de API configuradas.

---

## 🛠️ Como Instalar e Executar

### 1. Instalação de Dependências
```bash
./install.sh
# Ou manualmente:
pip install -r requirements.txt
```

### 2. Configurar Chaves de API (Opcional)
Crie um arquivo `.env` no diretório raiz do projeto (ou configure as variáveis de ambiente):
```env
GEMINI_API_KEY=sua_chave_gemini
GROK_API_KEY=sua_chave_grok
OPENAI_API_KEY=sua_chave_openai
DEFAULT_LLM_PROVIDER=gemini
```

### 3. Execução

- **Interface Gráfica Web**:
  ```bash
  python3 run.py web
  ```
  Acesse no navegador: `http://localhost:8000`

- **Executar Bateria de Testes (`pytest`)**:
  ```bash
  python3 run.py test
  ```

- **Verificar Diagnóstico de Conexão com APIs**:
  ```bash
  python3 run.py check
  ```

---

## 📁 Estrutura de Arquivos

```
AI_RPG_GAME/
├── engine/                      # Core Game Engine
│   ├── domain/                  # Domínio, regras e estado do jogo
│   ├── db/                      # Tabelas SQLite3 e busca por vetores (RAG)
│   ├── memory/                  # Builder de contexto, importance score e resumidor
│   └── providers/               # Provedores de IA (Gemini, Grok, OpenAI, Ollama)
├── server/                      # Servidor REST FastAPI para a Web UI
├── web/                         # Frontend Web em Glassmorphism (HTML/CSS/JS)
├── tests/                       # Bateria de testes pytest
├── check_api.py                 # Script diagnóstico de conexão das APIs
├── config.py                    # Configurações globais
└── run.py                       # Executável único de inicialização
```
