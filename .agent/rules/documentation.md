# Documentation Rules & Synchronization

## Source of Truth Hierarchy
1. `docs/architecture/`: Define a visão macro, limites de módulos, fluxo de dados e restrições.
2. `docs/domain/`: Define as entidades de negócio, regras do reino, métricas e modelo de dados.
3. `docs/decisions/` (ADR): Registra as decisões arquiteturais tomadas e suas justificativas (contexto, decisão, alternativas, consequências).
4. `docs/systems/`: Detalha fluxos específicos como execução de turnos, sumarização e import/export.
5. `docs/guides/`: Guias práticos de setup, extensão e testes.
6. `specs/`: Registra especificações ativas e históricas de features.

## Synchronization Triggers
A documentação DEVE ser atualizada sempre que:
1. Um novo módulo, tabela de banco de dados ou endpoint for criado.
2. O contrato de resposta do LLM ou formato de DTO for alterado.
3. Uma nova dependência externa for adicionada ao `requirements.txt` ou `config.py`.
4. Um novo provedor de LLM for adicionado ou a lógica de fallback for alterada.
5. Um fluxo de negócio (ex: cálculo de felicidade, sumarização de capítulos) for refatorado.

## Regras de Manutenção
- Nunca deixe a documentação defasada em relação ao código.
- Ao atualizar uma funcionalidade, execute a skill `update-docs` para identificar todos os arquivos de documentação impactados.
- Ao tomar uma nova decisão estrutural que altere o design do sistema, crie um novo ADR numerado sequencialmente em `docs/decisions/` (ex: `ADR-006-*.md`).
