---
name: implement-spec
description: Executa a implementação de uma funcionalidade a partir de uma especificação estruturada em specs/active/<feature>/, seguindo estritamente o design.md e marcando as tarefas em tasks.md.
---

# Skill: implement-spec

## Objetivo
Executar as tarefas planejadas de forma rigorosa, atômica e disciplinada, respeitando os contratos definidos em `design.md` sem introduzir padrões arquiteturais arbitrários ou desvios não documentados.

## Quando Utilizar
- Após a criação e aprovação de uma spec em `specs/active/<feature-name>/`.

## Regra de Ouro
**Nunca invente uma arquitetura diferente da definida em `design.md`.** Caso durante a codificação seja descoberto que o design original é inviável ou precisa de ajustes, pause a implementação, atualize `design.md` e `tasks.md`, e então retome o código.

## Fluxo de Execução

1. **Leitura da Spec**:
   - Inspecione `specs/active/<feature-name>/requirements.md`, `design.md` e `tasks.md`.

2. **Execução Sequencial por Camadas (Bottom-Up / TDD)**:
   - **Banco & Persistência**: Alterar schema/tabelas em `engine/db/schema.py` e métodos em `repository.py`.
   - **Domínio**: Criar/alterar dataclasses em `engine/domain/models.py` e lógica na `GameEngine`.
   - **Memória & Providers**: Ajustar contexto, importância ou provedores se necessário.
   - **API / DTOs**: Criar DTOs Pydantic em `server/dto.py` e endpoints em `server/app.py`.
   - **Apresentação**: Implementar componentes JS/CSS em `web/` se a feature envolver UI.

3. **Checklist Tracking**:
   - A cada tarefa concluída, marque o checkbox correspondente em `specs/active/<feature-name>/tasks.md` (`- [x]`).

4. **Sem Comentários**:
   - Mantenha o código estritamente sem comentários inline ou blocos de comentários, seguindo as diretrizes do projeto.

5. **Execução de Testes**:
   - Execute a suíte de testes com `pytest` para validar o correto funcionamento e assegurar que não haja regressões.
