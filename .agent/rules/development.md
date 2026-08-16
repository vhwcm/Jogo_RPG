# Development Workflow & Task Sizing

## 1. Classificação do Tamanho da Tarefa

Antes de iniciar qualquer tarefa, avalie sua complexidade e escopo:

### Tarefa Pequena (Small)
- **Critérios**: Correções de digitação, bugs triviais isolados, refatoração de função simples, ajustes visuais pontuais.
- **Ação**: 
  1. Identificar o ponto exato da alteração.
  2. Implementar sem comentários no código.
  3. Executar testes pertinentes (`pytest`).
  4. Atualizar documentação apenas se houver impacto funcional visível.
  5. Criar commit descritivo e executar `git push`.

### Tarefa Média (Medium)
- **Critérios**: Novo endpoint REST, novo método de repositório, novo componente de interface, novo provider de LLM.
- **Ação**:
  1. Consultar a documentação em `docs/` e regras de arquitetura.
  2. Elaborar um plano de tarefas atômico (diretamente no raciocínio ou em mini-spec).
  3. Implementar seguindo TDD e princípios SOLID.
  4. Validar com testes unitários.
  5. Atualizar documentação afetada em `docs/`.
  6. Criar commit descritivo e executar `git push`.

### Tarefa Grande (Large)
- **Critérios**: Novo sistema do jogo (ex: combate, comércio, facções), mudanças de schema no SQLite, modificações no motor RAG, refatorações amplas.
- **Ação**:
  1. **Explore**: Executar `explore-project` para mapear dependências e restrições.
  2. **Spec**: Criar especificação completa em `specs/active/<feature-name>/` com `requirements.md`, `design.md` e `tasks.md`.
  3. **Implement**: Executar `implement-spec` tarefa por tarefa sem desviar do `design.md`.
  4. **Test**: Executar suíte completa de testes.
  5. **Review**: Executar `review-consistency` para auditoria cruzada.
  6. **Update Docs**: Executar `update-docs` para atualizar o conhecimento persistente do projeto e criar novos ADRs se cabível.
  7. **Archive**: Mover a spec para `specs/completed/<feature-name>/`.
  8. **Commit & Push**: Criar commit descritivo e executar `git push`.
