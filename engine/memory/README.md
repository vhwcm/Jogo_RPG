# 🧠 Submódulo Memory (`engine/memory`)

O submódulo `engine/memory` gerencia o ciclo de vida cognitivo e de memória do RPG, impedindo a perda de coerência temporal e a explosão de tokens em campanhas de longa duração.

---

## 📂 Arquivos do Módulo

- **`context_builder.py`**: Compilador de contexto dinâmico que injeta na IA apenas as informações mais pertinentes para a decisão atual do jogador.
- **`importance.py`**: Algoritmo de classificação de relevância e importância (0.0 a 1.0) para eventos narrativos e decisões críticas.
- **`summarizer.py`**: Agente de compressão histórica periódica que consolida turnos passados em resumos hierárquicos e capítulos densos.

---

## 🏗️ As 4 Camadas de Memória

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Memória de Curto Prazo (Janela imediata dos últimos turnos)│
├─────────────────────────────────────────────────────────────┤
│ 2. Estado Estruturado (Tabelas de Recursos, Itens e Tasks)  │
├─────────────────────────────────────────────────────────────┤
│ 3. Memória Episódica RAG (Top-K Embeddings + Score Relevância)│
├─────────────────────────────────────────────────────────────┤
│ 4. Resumo de Longo Prazo (Capítulos Históricos Comprimidos) │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Detalhes dos Componentes

### 1. `ContextBuilder`
Monta o prompt enriquecido combinando:
- O estado atual dos recursos e religião do reino.
- A lista de patrimônio ativo (estruturas, postos avançados, monumentos, itens).
- Tarefas em andamento e incidentes dinâmicos com progresso.
- Status diplomático dos reinos vizinhos.
- Memórias episódicas resgatadas pelo `VectorStore` via similaridade semântica da ação do jogador.
- NPCs e personagens relevantes.

### 2. `importance.py`
Analisa o impacto dos acontecimentos através de heurísticas de palavras-chave e alterações de estado:
- Mortes de personagens e declarações de guerra: **0.8 - 1.0**
- Conquistas territoriais, novas construções e alianças: **0.6 - 0.8**
- Gestão diária de recursos e diálogos triviais: **0.2 - 0.5**

### 3. `CampaignSummarizer`
A cada intervalo de turnos (ex: a cada 10 turnos), condensa o histórico anterior sem perder os fatos canônicos, atualizando o campo `summary` na tabela `campaigns`.
