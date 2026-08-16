---
name: review-consistency
description: Realiza uma auditoria cruzada de consistência entre Requirements, Design, Tasks, Código Implementado, Testes e Documentação para prevenir desvios ou divergências.
---

# Skill: review-consistency

## Objetivo
Detectar e corrigir discrepâncias entre o que foi planejado, o que foi implementado, o que está testado e o que está documentado no repositório.

## Matriz de Auditoria de Consistência

```
Requirements  ◄──────►  Design  ◄──────►  Tasks
     ▲                                      ▲
     │                                      │
     ▼                                      ▼
    Code      ◄──────►   Docs   ◄──────►  Tests
```

## Quando Utilizar
- Antes de finalizar a implementação de uma spec ou feature.
- Em revisões de código (code reviews) e auditorias de qualidade.
- Sempre que houver suspeita de desalinhamento entre documentação e código real.

## Checklist de Verificação

1. **Requirements ↔ Design**:
   - Cada requisito funcional (`R1`, `R2`, ...) possui componentes e fluxo técnico correspondentes no `design.md`?
   - Os critérios de aceite são viáveis e contemplados na arquitetura proposta?

2. **Design ↔ Tasks**:
   - Todas as alterações de banco, modelo, API e UI projetadas no `design.md` estão presentes como itens em `tasks.md`?

3. **Tasks ↔ Code**:
   - Todas as tarefas marcadas como concluídas (`- [x]`) foram efetivamente implementadas no código?
   - O código não introduziu classes ou lógicas "fantasmas" que não constavam no design?

4. **Code ↔ Docs**:
   - O banco de dados real em `engine/db/schema.py` corresponde ao documentado em `docs/architecture/database.md`?
   - Os endpoints reais em `server/app.py` correspondem a `docs/architecture/backend.md`?
   - Os modelos de domínio em `engine/domain/models.py` correspondem aos listados em `docs/domain/`?

5. **Code ↔ Tests**:
   - Existem testes unitários cobrindo os caminhos principais e de exceção das novas funções/endpoints?
   - A suíte de testes executa com 100% de aprovação (`pytest`).

6. **Relatório de Consistência**:
   - Se forem detectadas divergências, listar as inconsistências encontradas e corrigir o código ou a documentação antes de concluir a entrega.
