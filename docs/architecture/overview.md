# 🏛️ Architecture Overview

## 1. Stack Tecnológica
- **Backend Core**: Python 3.10+ com Clean Layered Architecture.
- **API Server**: FastAPI (Uvicorn ASGI) com validação de contratos via Pydantic v2.
- **Banco de Dados**: SQLite3 (modo WAL, foreign keys ativas) com consultas determinísticas e repositório centralizado.
- **Vector & Memory Engine**: RAG episódico com cosine similarity (NumPy/Pure Python) + cálculo de importância e sumarização hierárquica.
- **Provedores de IA**: Google Gemini (padrão), xAI Grok, OpenAI, Ollama Local e Mock Fallback, orquestrados por `LLMFactory`.
- **Frontend Presentation**: Single Page Application (HTML5, Vanilla CSS3 com estética Glassmorphism, Vanilla JS ES6+).
- **Áudio Dinâmico**: Web Audio API com transições adaptativas por estado de `clima`.

---

## 2. Diagrama de Componentes e Camadas

```
┌─────────────────────────────────────────────────────────────┐
│                 Web Presentation Layer (SPA)                │
│       (HTML5 / Glassmorphism CSS / Vanilla JS / Audio)      │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP REST (JSON)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Server API Layer (FastAPI)                │
│              (server/app.py & server/dto.py)                │
└──────────────────────────────┬──────────────────────────────┘
                               │ Injeção de Dependência
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Domain & Orchestration (GameEngine)           │
│           (engine/domain/state_manager.py & models.py)      │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
┌──────────────────────────────┐ ┌─────────────────────────────┐
│    Memory & Context Builder  │ │     LLM Provider Layer      │
│  (engine/memory/context_*)   │ │  (engine/providers/factory) │
└──────────────┬───────────────┘ └─────────────┬───────────────┘
               │                               │
               ▼                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Persistence & Storage Layer                 │
│      (engine/db/repository.py & vector_store.py SQLite3)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Fluxo de Dados (Data Flow)

1. **Entrada do Jogador**: O usuário seleciona uma opção ou digita uma ação livre na interface Web/CLI.
2. **Recepção HTTP**: A camada `server/` valida o payload através de `TurnRequestDTO` e despacha para `GameEngine.execute_turn()`.
3. **Construção de Contexto (ContextBuilder)**:
   - Recupera o estado atual do reino (`world_state`).
   - Carrega o sumário histórico de capítulos (`campaigns.summary`).
   - Executa busca vetorial RAG no `VectorStore` para recuperar memórias episódicas mais relevantes.
   - Monta o prompt contextualizado para o Game Master.
4. **Inferência LLM**: `LLMFactory` seleciona o provedor ativo (com fallback automático caso haja indisponibilidade) e retorna um payload estruturado em JSON.
5. **Processamento e Validação**:
   - `GameEngine` sanitiza e valida as métricas numéricas (ouro, população, poder militar, felicidade, clima).
   - Atualiza entidades secundárias (personagens, quests, itens) se fornecidas.
6. **Persistência**: Grava o novo estado em `world_state`, a nova memória vetorizada em `memories` e verifica se atingiu o gatilho de sumarização periódica (`CampaignSummarizer`).
7. **Resposta**: Retorna `TurnResponseDTO` serializado para a interface do jogador.

---

## 4. Princípios Arquiteturais

1. **Separação Estrita de Responsabilidades (SoC)**: O domínio do jogo desconhece a camada de transporte (HTTP/CLI).
2. **Resiliência e Fallback**: Nenhuma falha temporária de API de IA interrompe o jogo; o `FallbackLLMProvider` tenta provedores subsequentes até o mock seguro.
3. **Persistência Determinística**: Valores numéricos e entidades são armazenados em tabelas relacionais no SQLite, nunca delegados puramente à "memória" alucinatória de um modelo de linguagem.
4. **Eficiência de Contexto**: A memória episódica RAG e a sumarização hierárquica garantem que campanhas de centenas de turnos permaneçam dentro de uma janela de contexto enxuta e barata.

---

## 5. Limites e Restrições Invioláveis

- Nenhuma query SQL fora de `engine/db/`.
- Nenhuma regra de negócio de jogo dentro de `server/app.py`.
- Todas as configurações e variáveis de ambiente obrigatoriamente lidas através de `config.py`.
