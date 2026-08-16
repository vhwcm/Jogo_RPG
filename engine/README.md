# ⚙️ Módulo Engine (Motor Central do RPG)

O módulo `engine` é o núcleo lógico e arquitetural do **AI RPG Game**. Ele implementa a lógica do jogo seguindo os princípios de **Clean Architecture** e **Hexagonal Architecture**, orquestrando o estado do mundo, o banco de dados relacional e vetorial, a inteligência artificial (LLMs) e a recuperação de contexto em memória episódica (RAG).

---

## 📂 Estrutura do Diretório

```
engine/
├── db/            # Camada de persistência SQLite, Repositório e Vector Store
├── domain/        # Modelos de domínio (Dataclasses) e Gerenciador de Estado do Jogo (GameEngine)
├── memory/        # Sistema de memória (Context Builder, Importance Scoring e Summarizer)
├── providers/     # Camada de abstração e clientes de Provedores de LLM (Gemini, Grok, OpenAI, Ollama)
├── utils.py       # Utilitários de sanitização de JSON, extração de texto e parsing de responses
└── __init__.py
```

---

## 🎯 Principais Responsabilidades

1. **Gestão do Ciclo de Turnos**: Recebe as ações do soberano/jogador, consulta a memória histórica do mundo e coordena a geração do próximo turno narrativo pela IA.
2. **Desacoplamento de Provedores de IA**: Permite alternar dinamicamente entre Google Gemini, xAI Grok, OpenAI e Ollama local sem alterar uma única linha da lógica de negócio.
3. **Persistência Estruturada & Vetorial (RAG)**: Salva métricas relacionais (ouro, população, poder militar, felicidade, religião, patrimônio, tarefas e alianças) e calcula embeddings de eventos narrativos para recuperação semântica.
4. **Execução de Ações Atômicas**: Processa mutações no mundo disparadas pela IA através do protocolo de `GameAction` (criação de estruturas, entrega de itens, abertura de tarefas e mudanças diplomáticas).

---

## 🚀 Exemplo de Uso Programático

```python
from engine.domain.state_manager import GameEngine
from engine.providers.factory import LLMFactory

# Inicializa o motor do jogo
engine = GameEngine()

# Cria uma nova campanha
turn = engine.create_campaign(
    campaign_name="Crônicas de Eldoria",
    ruler_name="Imperador Valerius",
    kingdom_name="Reino de Eldoria",
    race="Humano"
)

# Processa o próximo turno com a decisão do jogador
proximo_turno = engine.process_turn(
    campaign_id=engine.current_campaign_id,
    player_input="Construir um posto de vigia nas colinas do leste e treinar arqueiros."
)
```
