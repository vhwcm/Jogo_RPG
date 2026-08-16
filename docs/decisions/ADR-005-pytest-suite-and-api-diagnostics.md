# ADR-005: Suíte Abrangente de Testes Pytest e Diagnóstico de Conectividade

* **Status**: Aceito
* **Data**: 2026-08-15
* **Decisores**: Equipe de Desenvolvimento AI RPG

## Contexto
Mudanças no motor de RAG, contratos JSON do LLM ou rotas de API podem introduzir regressões silenciosas sem uma suíte de testes automatizados e ferramentas de diagnóstico de credenciais.

## Decisão
1. Adotar **Pytest** cobrindo todos os subsistemas (`tests/test_*.py`):
   - Banco de dados SQLite e integridade referencial (`test_db.py`).
   - Busca vetorial de semântica e cálculo de relevância (`test_vector_store.py`).
   - Abstração e fallbacks de provedores de IA (`test_providers.py`).
   - Orquestração de campanhas e rollbacks (`test_domain.py`).
   - Contratos de rotas HTTP e serialização de DTOs (`test_api.py`).
2. Criar script autônomo `check_api.py` para testar chaves de API reais, latência de inferência e suporte a JSON estruturado.

## Alternativas Consideradas
- **Testes Manuais**: Propensos a falhas e lentos para validar fluxos multi-turnos.
- **Unittest padrão do Python**: Menos expressivo e com fixtures menos flexíveis que o Pytest.

## Consequências
- **Positivas**:
  - Confiança imediata em refatorações e adições de features.
  - Execução rápida (<2 segundos) da suíte inteira.
- **Negativas**:
  - Exige manutenção contínua de fixtures caso schemas sofram breaking changes.
