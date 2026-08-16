# 📋 Specifications System (Specs)

Este diretório implementa o sistema de especificações e planejamento inspirado na filosofia do Kiro.

---

## Estrutura de Diretórios

```
specs/
├── template/
│   ├── requirements.md   — Modelo para definição de escopo e requisitos
│   ├── design.md         — Modelo para decisões de arquitetura e design técnico
│   └── tasks.md          — Modelo para checklist atômico de implementação
├── active/               — Especificações de funcionalidades atualmente em desenvolvimento
└── completed/            — Especificações de funcionalidades já implementadas, testadas e arquivadas
```

---

## Ciclo de Vida de uma Spec

1. **Criação**: Criar subdiretório em `specs/active/<feature-name>/` copiando os templates de `specs/template/`.
2. **Definição de Requisitos (`requirements.md`)**: Registrar o objetivo de negócio, requisitos funcionais (`R1`, `R2`, ...) e critérios de aceite.
3. **Design Técnico (`design.md`)**: Projetar as alterações em Domínio, Banco de Dados, API, UI, tratamento de erros e testes.
4. **Lista de Tarefas (`tasks.md`)**: Decompor o design em itens atômicos e sequenciais.
5. **Implementação**: Executar as tarefas marcando o progresso no checklist (`- [x]`).
6. **Revisão e Sincronização**: Executar as skills `review-consistency` e `update-docs`.
7. **Arquivamento**: Mover a pasta da spec de `specs/active/<feature-name>` para `specs/completed/<feature-name>`.
