---
name: create-spec
description: Cria uma especificação completa e estruturada (requirements.md, design.md, tasks.md) em specs/active/<feature>/ antes de implementar uma funcionalidade média ou grande.
---

# Skill: create-spec

## Objetivo
Separar a fase de concepção e planejamento da fase de codificação (`THINK -> SPEC -> IMPLEMENT`), garantindo que requisitos, arquitetura técnica e lista de tarefas estejam claramente definidos antes de qualquer modificação de código.

## Quando Utilizar
- Sempre que for solicitada uma feature média ou grande.
- Ao planejar refatorações de grande escala ou mudanças de banco de dados.

## Fluxo de Execução

1. **Definição do Diretório da Spec**:
   - Crie o diretório `specs/active/<feature-name>/`.

2. **Criação de `requirements.md`**:
   - Detalhe o objetivo principal (`Goal`).
   - Enumere os Requisitos Funcionais de forma atômica (`R1`, `R2`, ...).
   - Defina Requisitos Não-Funcionais (performance, compatibilidade).
   - Estabeleça Critérios de Aceite verificáveis em formato de checkbox.

3. **Criação de `design.md`**:
   - Especifique a arquitetura do componente e onde ele se encaixa na Clean Architecture.
   - Inclua diagramas **D2** para modelar o fluxo de dados, interações entre componentes ou processos de negócio.
   - Detalhe novos modelos em `engine/domain/models.py` (dataclasses).
   - Detalhe novos DTOs em `server/dto.py` (Pydantic).
   - Detalhe alterações no banco SQLite (`engine/db/schema.py`, `repository.py`).
   - Detalhe novos endpoints REST ou componentes de UI.
   - Defina os **pontos de observabilidade e logs estruturados** (eventos, contexto, níveis de log).
   - Defina a estratégia de tratamento de erros e resiliência.
   - Defina a estratégia de testes unitários (`pytest`).

4. **Criação de `tasks.md`**:
   - Crie uma lista atômica, sequencial e executável de tarefas.
   - Cada tarefa deve representar uma unidade de trabalho mensurável (ex: migration, modelo de domínio, método de repositório, rota na API, instrumentação de logs, diagramas D2, testes, atualização de doc).

5. **Validação Preliminar**:
   - Garanta que nenhuma decisão em `design.md` viole as regras de `AGENTS.md` ou os ADRs em `docs/decisions/`.
   - Apresente a spec para o usuário ou prossiga para a implementação quando aprovada.

