# ADR 0003: Provedores de LLM Plugáveis com Descoberta Automática de Modelos & Testes de Probe

* **Status**: Aceito (Atualizado)
* **Data**: 2026-08-15
* **Autor**: Antigravity AI & Usuário

## 📋 Contexto

Modelos de linguagem evoluem rapidamente e nomes hardcoded de modelos (como `gemini-2.5-flash` ou `text-embedding-004`) podem tornar-se obsoletos ou ter nomes ligeiramente alterados na API pública de cada provedor. O jogo precisa listar dinamicamente os modelos disponíveis, selecionar automaticamente o mais recente e testar com uma chamada de probe real para garantir que há resposta antes de aceitá-lo no ciclo principal.

## 🎯 Decisão

1. Implementar o método `discover_and_test_models()` no `GeminiProvider` (e abstrações equivalentes) que:
   - Consulta a API (`models.list()` / `list_models()`) para descobrir todos os modelos ativados na conta do usuário.
   - Ordena os modelos candidatos por versão recente (ex: `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`).
   - Executa uma **Requisição de Probe ao Vivo** (`generate_text("Diga OK")`) para testar a conectividade e resposta do modelo.
   - Define o modelo que respondeu com sucesso como o modelo ativo da partida.
   - Executa probe equivalente para a geração de **Embeddings Vetoriais** (`text-embedding-004`, `embedding-001`).
2. Atualizar o script de diagnóstico (`python3 run.py check`) para exibir o nome exato do modelo descoberto e testado.

## ⚡ Consequências

- **Positivas**:
  - Resiliência total contra desativação ou depreciação de versões antigas de modelos.
  - Seleção automática da versão de modelo mais recente e rápida da API.
  - Teste imediato de sanidade ao iniciar a aplicação.
- **Negativas**:
  - Adiciona ~200ms a 500ms no tempo de inicialização da primeira instância do provedor para a execução do probe de verificação.
