# Documentation Rules & Synchronization

## Source of Truth Hierarchy
1. `docs/architecture/`: Define a visão macro, limites de módulos, fluxo de dados e restrições (com diagramas D2).
2. `docs/diagrams/`: Diagramas visuais D2 de arquitetura, fluxos de dados, componentes e processos de negócio.
3. `docs/domain/`: Define as entidades de negócio, regras do reino, métricas e modelo de dados.
4. `docs/decisions/` (ADR): Registra as decisões arquiteturais tomadas e suas justificativas (contexto, decisão, alternativas, consequências, diagramas D2).
5. `docs/systems/`: Detalha fluxos específicos como execução de turnos, sumarização e import/export (acompanhados de diagramas D2 de fluxo).
6. `docs/guides/`: Guias práticos de setup, extensão, testes, observabilidade e procedimentos de troubleshooting.
7. `specs/`: Registra especificações ativas e históricas de features com design D2.

## Synchronization Triggers
A documentação DEVE ser atualizada sempre que:
1. Um novo módulo, tabela de banco de dados ou endpoint for criado.
2. O contrato de resposta do LLM ou formato de DTO for alterado.
3. Uma nova dependência externa for adicionada ao `requirements.txt` ou `config.py`.
4. Um novo provedor de LLM for adicionado ou a lógica de fallback for alterada.
5. Um fluxo de negócio (ex: cálculo de felicidade, sumarização de capítulos) for refatorado.
6. Um fluxo de dados, interação de componentes ou processo assíncrono for criado ou modificado (exige criação ou atualização de diagrama D2 correspondente).
7. Um procedimento de troubleshooting recorrente for identificado e solucionado.

## Regras de Manutenção
- Nunca deixe a documentação ou diagramas D2 defasados em relação ao código.
- Toda modificação de arquitetura ou fluxo deve atualizar o respectivo diagrama D2 referenciado.
- Ao atualizar uma funcionalidade, execute a skill `update-docs` para identificar todos os arquivos de documentação e diagramas D2 impactados.
- Ao tomar uma nova decisão estrutural que altere o design do sistema, crie um novo ADR numerado sequencialmente em `docs/decisions/` (ex: `ADR-006-*.md`).

