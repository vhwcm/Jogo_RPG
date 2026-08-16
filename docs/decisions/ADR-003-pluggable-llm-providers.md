# ADR-003: Provedores Plugáveis de LLM com Cadeia de Fallback e Auto-Discovery

* **Status**: Aceito
* **Data**: 2026-08-15
* **Decisores**: Equipe de Desenvolvimento AI RPG

## Contexto
APIs de inteligência artificial sofrem com rate limits, quotas esgotadas, variações de nomenclatura de modelos e indisponibilidades transitórias. O jogo não pode travar ou perder a partida caso o provedor principal apresente erro temporário.

## Decisão
1. Implementar interface comum `BaseLLMProvider` e fábrica `LLMFactory`.
2. Encapsular as chamadas em `FallbackLLMProvider`, que tenta em cascata: Provedor Selecionado (ex: Gemini) → Demais Provedores Configurados (Grok, OpenAI, Ollama) → `MockFallbackProvider`.
3. Adicionar probe de modelos (`discover_and_test_models()`) para validar conectividade e suporte a embeddings antes de aceitar o modelo no loop principal.

## Alternativas Consideradas
- **Provedor Único Hardcoded**: Frágil a oscilações de rede ou esgotamento de créditos.
- **LangChain / LlamaIndex**: Frameworks pesados com frequentes breaking changes e abstrações opacas.

## Consequências
- **Positivas**:
  - Resiliência total a falhas de APIs externas.
  - Facilidade de adicionar novos provedores (ex: Anthropic, Mistral).
  - Testabilidade com mock determinístico em ambiente CI.
- **Negativas**:
  - Pequeno overhead de latência caso um provedor falhe e precise acionar o próximo na cadeia.
