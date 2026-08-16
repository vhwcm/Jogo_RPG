# 📖 System: Hierarchical Campaign Summarizer

## Overview
O `CampaignSummarizer` impede a explosão de tokens em campanhas longas ao condensar blocos de 10 turnos em resumos estruturados ("Capítulos de Crônica"), que são salvos na tabela `campaigns`.

---

## Gatilho e Funcionamento (`engine/memory/summarizer.py`)

1. **Gatilho de Disparo**:
   - A cada `config.SUMMARY_INTERVAL_TURNS` (padrão: 10 turnos), o método `summarize_if_needed(campaign_id, current_turn)` é acionado.
2. **Coleta de Memórias**:
   - Coleta os eventos e memórias ocorridos nos últimos 10 turnos.
3. **Chamada de Sumarização**:
   - Dispara um prompt especializado para o LLM instruindo-o a resumir os acontecimentos em estilo cronista medieval, preservando:
     - Nomes próprios e títulos.
     - Vitórias e derrotas militares.
     - Mortes, alianças ou traições.
     - Grandes obras ou desastres naturais.
4. **Persistência Acumulada**:
   - O novo resumo é apensado ao campo `summary` da tabela `campaigns`.
5. **Uso no ContextBuilder**:
   - O `summary` é inserido no início de todos os prompts subsequentes, permitindo que a IA conheça o passado de 50 ou 100 turnos atrás gastando apenas ~300 tokens de contexto.
