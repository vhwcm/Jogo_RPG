# Development Workflow & Task Sizing

## 1. Classificação do Tamanho da Tarefa

Antes de iniciar qualquer tarefa, avalie sua complexidade e escopo:

### Tarefa Pequena (Small)
- **Critérios**: Correções de digitação, bugs triviais isolados, refatoração de função simples, ajustes visuais pontuais.
- **Ação**: 
  1. Identificar o ponto exato da alteração (consultando logs caso seja um bug de runtime).
  2. Implementar sem comentários no código, mantendo ou adicionando logs estruturados pertinentes.
  3. Executar testes pertinentes (`pytest`).
  4. Atualizar documentação e diagramas D2 apenas se houver impacto funcional visível.
  5. Criar commit descritivo e executar `git push`.

### Tarefa Média (Medium)
- **Critérios**: Novo endpoint REST, novo método de repositório, novo componente de interface, novo provider de LLM.
- **Ação**:
  1. Consultar a documentação em `docs/` e diagramas D2 existentes.
  2. Elaborar um plano de tarefas atômico com previsão de logs estruturados e diagramas D2.
  3. Implementar seguindo TDD, princípios SOLID e instrumentação de logs estruturados.
  4. Validar com testes unitários.
  5. Atualizar documentação afetada em `docs/` e gerar/atualizar diagramas D2 correspondentes.
  6. Criar commit descritivo e executar `git push`.

### Tarefa Grande (Large)
- **Critérios**: Novo sistema do jogo (ex: combate, comércio, facções), mudanças de schema no SQLite, modificações no motor RAG, refatorações amplas.
- **Ação**:
  1. **Explore**: Executar `explore-project` para mapear dependências, diagramas D2 e restrições.
  2. **Spec**: Criar especificação completa em `specs/active/<feature-name>/` com `requirements.md`, `design.md` (incluindo diagramas D2 e pontos de observabilidade) e `tasks.md`.
  3. **Implement**: Executar `implement-spec` tarefa por tarefa sem desviar do `design.md`, com logs estruturados completos.
  4. **Test**: Executar suíte completa de testes.
  5. **Review**: Executar `review-consistency` para auditoria cruzada (Code ↔ Tests ↔ Docs ↔ D2 ↔ Logs).
  6. **Update Docs**: Executar `update-docs` para atualizar o conhecimento persistente do projeto, diagramas D2, guias de troubleshooting e criar novos ADRs se cabível.
  7. **Archive**: Mover a spec para `specs/completed/<feature-name>/`.
  8. **Commit & Push**: Criar commit descritivo e executar `git push`.

## 2. Diretrizes de Troubleshooting
- **Uso Obrigatório de Logs**: Nunca tente adivinhar causas raízes apenas inspecionando código; consulte e analise os logs estruturados emitidos pelo sistema.
- **Reutilização de Procedimentos**: Consulte `docs/guides/observability_and_troubleshooting.md` para procedimentos conhecidos e documente novas rotinas descobertas.

