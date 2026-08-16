# Git Workflow, Commit & Push

## 1. Ciclo Obrigatório de Versionamento

Sempre após concluir alterações no código, tarefas, correções de bugs, refatorações ou documentação:

1. **Verificação de Status e Diffs**:
   - Inspecione `git status` e `git diff` para garantir que apenas os arquivos pretendidos e pertinentes à alteração sejam incluídos no commit.
   - Nunca adicione arquivos temporários de banco de dados (ex: `-shm`, `-wal`), caches ou logs.

2. **Commit Descritivo e Semântico**:
   - Crie commits atômicos com mensagens claras e objetivas.
   - Siga convenções semânticas claras (ex: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`).
   - O título e corpo do commit devem explicar exatamente o que foi modificado e o motivo.

3. **Push Imediato**:
   - Após criar o commit, execute imediatamente `git push` para sincronizar o repositório remoto (`origin <branch>`).
