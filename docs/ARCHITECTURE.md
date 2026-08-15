# 🏛️ Visão Geral da Arquitetura do Sistema

O **AI RPG Game** foi construído seguindo princípios de **Clean Architecture** e **Hexagonal Architecture**, desacoplando totalmente a lógica do domínio de jogo, persistência e inferências de IA das camadas de apresentação (CLI Terminal e Web Application).

---

## 🎯 Diagrama de Componentes

```
                     ┌──────────────────────────┐
                     │    Interface CLI (Rich)  │
                     └─────────────┬────────────┘
                                   │
┌──────────────────────────┐       │
│  Interface Web (HTML/JS) ├───────┼───────────────────────┐
└────────────┬─────────────┘       │                       │
             │                     │                       │
             ▼                     ▼                       ▼
    ┌─────────────────────────────────────────────────────────────┐
    │              FastAPI Server / Engine Controller             │
    └──────────────────────────────┬──────────────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
     ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
     │ World State Mgr  │ │ Context Builder  │ │ Modular LLMs     │
     │ (Domain Logic)   │ │ & Memory Layer   │ │ (Gemini/Grok/...)│
     └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
              │                    │                    │
              ▼                    ▼                    ▼
     ┌──────────────────────────────────────────────────────────┐
     │              SQLite3 Storage & Vector RAG                │
     └──────────────────────────────────────────────────────────┘
```

---

## 🧠 Arquitetura de Memória em 4 Camadas

1. **Memória de Curto Prazo (Short-Term Context Window)**: Retém as últimas 4 a 10 interações diretas do diálogo atual para manter a fluidez imediata do turno.
2. **Estado Estruturado do Mundo (Structured SQLite State)**: Guarda em tabelas relacionais os valores exatos de ouro, população, poder militar, felicidade, religião, lealdade de personagens e status de quests.
3. **Memória Episódica RAG (Vector Similarity + Importance)**: Eventos relevantes são vetorizados (embeddings) e armazenados no SQLite3 com um score de importância (0.0 a 1.0). Na hora de responder, o sistema busca os 5 acontecimentos mais pertinentes semanticamente para a ação do jogador.
4. **Resumo Hierárquico de Campanhas (Campaign Chapter Compression)**: A cada 10 turnos, um summarizer de IA comprime o histórico anterior em capítulos densos, impedindo a explosão de tokens em campanhas longas.

---

## 🗄️ Esquema do Banco de Dados SQLite3

- `campaigns`: Registro de campanhas (`id`, `name`, `summary`, `created_at`).
- `world_state`: Histórico de turnos do reino (`campaign_id`, `turn_number`, `kingdom_name`, `ruler_name`, `race`, `gold`, `population`, `military`, `happiness`, `religion`).
- `characters`: Personagens e NPCs (`id`, `name`, `role`, `location`, `is_alive`, `relationship_with_player`, `knowledge_json`).
- `quests`: Missões do reino (`id`, `title`, `description`, `status`, `objective`).
- `memories`: Vetores e eventos RAG (`id`, `turn_number`, `content`, `importance`, `embedding_json`, `characters_json`).
