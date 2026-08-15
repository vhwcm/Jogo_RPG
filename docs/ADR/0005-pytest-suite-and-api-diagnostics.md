# ADR 0005: Estratégia de Testes Pytest e Diagnóstico de APIs

* **Status**: Aceito
* **Data**: 2026-08-15
* **Autor**: Antigravity AI & Usuário

## 📋 Contexto

O código antigo não possuía bateria de testes automatizados nem verificações de integridade de API, dificultando a identificação de quebras ao modificar regras de jogo ou chaves de API. O usuário solicitou que houvesse sempre muitos testes para cobrir todas as funcionalidades e um script de verificação da API.

## 🎯 Decisão

1. Implementar uma suíte completa de testes unitários e de integração utilizando **`pytest`** na pasta `tests/` cobrindo:
   - Esquema de banco de dados e repositórios CRUD (`test_db.py`).
   - Algoritmo de semântica vetorial e calculador de importância (`test_vector_store.py`).
   - Abstração e fallbacks dos provedores de LLM, incluindo Grok (`test_providers.py`).
   - Ciclo de vida da campanha no domínio (`test_domain.py`).
   - Endpoints HTTP do servidor REST (`test_api.py`).
2. Criar o utilitário **`check_api.py`** que testa individualmente cada provedor (Gemini, Grok, OpenAI, Ollama), medindo latência e confirmando o suporte a JSON e embeddings.

## ⚡ Consequências

- **Positivas**:
  - Garantia de regressão zero a cada mudança no código.
  - Verificação instantânea da saúde das chaves de API antes de iniciar campanhas.
- **Negativas**:
  - Necessidade de manter os mocks atualizados caso a assinatura das respostas mude no futuro.
