# Resumo: Regra de Commit Descritivo e Push Obrigatório

## Objetivo
Adicionar e formalizar a regra no fluxo de trabalho do projeto para que, após qualquer modificação de código (seja tarefa pequena, média ou grande), seja realizado um commit descritivo/semântico e o respectivo `git push`.

---

## Modificações Realizadas

1. **[.agent/rules/git-workflow.md](file:///home/exati/AI_RPG_GAME/.agent/rules/git-workflow.md)**:
   - Criada regra dedicada especificando:
     - Verificação de arquivos e `git status` / `git diff` antes de commitar (evitando arquivos temporários como `-shm`, `-wal`, caches).
     - Formatação de commits semânticos e descritivos (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`).
     - Execução imediata de `git push` após o commit.

2. **[AGENTS.md](file:///home/exati/AI_RPG_GAME/AGENTS.md)**:
   - Adicionado o item `Commit Descritivo e Push Obrigatório` na seção de **Regras Críticas e Invioláveis**.

3. **[.agent/rules/development.md](file:///home/exati/AI_RPG_GAME/.agent/rules/development.md)**:
   - Atualizado o checklist de execução de tarefas **Small**, **Medium** e **Large**, incluindo o passo final obrigatório de criação de commit descritivo e execução do `git push`.

4. **Compatibilidade de Configurações**:
   - Criado symlink `.agents -> .agent` para garantir descoberta automática independente do resolvedor de regras do workspace.
