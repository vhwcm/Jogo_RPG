---
name: update-docs
description: Sincroniza e atualiza a base de documentação persistente em docs/ após alterações de código, criação de novos subsistemas, mudanças de banco de dados ou decisões arquiteturais.
---

# Skill: update-docs

## Objetivo
Manter a documentação do projeto como reflexo fiel e atualizado do código-fonte, garantindo que o agente e a equipe mantenham uma memória persistente e confiável de todo o sistema.

## Quando Utilizar
- Ao concluir a implementação de uma spec ou feature média/grande.
- Sempre que houver alteração em modelos de domínio, contratos de API, schemas de banco ou fluxos de execução.
- Ao tomar novas decisões de arquitetura ou adotar novas tecnologias.

## Fluxo de Decisão e Mapeamento

```
                 Código ou Arquitetura Mudou?
                             │
                             ▼
                    ┌─────────────────┐
                    │    Avaliação    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┬────────────────────┐
        ▼                    ▼                    ▼                    ▼
Domínio/Modelos?      Arquitetura/API/D2?    Nova Decisão?      Troubleshooting?
        │                    │                    │                    │
        ▼                    ▼                    ▼                    ▼
Atualizar docs/domain/ Atualizar docs/arch/,  Criar novo ADR em  Atualizar docs/guides/
                       docs/diagrams/ e D2    docs/decisions/    observability_*.md
```

## Checklist de Atualização por Área:

1. **Modelos de Domínio (`docs/domain/`)**:
   - Foram adicionadas novas entidades ou atributos a `KingdomStatus`, `Character`, `Quest`, `Item`?
   - Atualize os arquivos correspondentes em `docs/domain/`.

2. **Arquitetura, Diagramas D2 & Sistemas (`docs/architecture/`, `docs/diagrams/`, `docs/systems/`)**:
   - Foram criados novos endpoints REST em `server/app.py`?
   - O fluxo de execução de turnos, sumarização ou tratamento de erro mudou?
   - Verifique e atualize os **diagramas D2** correspondentes para refletir com exatidão os componentes e fluxos atuais.
   - Atualize `docs/architecture/backend.md`, `docs/systems/turn_execution.md`, etc.

3. **Banco de Dados (`docs/architecture/database.md`)**:
   - Houve inclusão de tabelas, índices ou colunas em `engine/db/`?
   - Atualize o diagrama D2/ERD e a descrição de schema.

4. **Decisões Arquiteturais (`docs/decisions/`)**:
   - Uma decisão estrutural foi alterada ou um novo padrão foi introduzido?
   - Crie um novo registro sequencial: `ADR-00X-<nome-da-decisao>.md` acompanhado de diagrama D2 se aplicável.

5. **Observabilidade & Procedimentos de Troubleshooting (`docs/guides/`)**:
   - Foi identificado um procedimento recorrente de investigação ou diagnóstico?
   - Documente a rotina passo a passo em `docs/guides/observability_and_troubleshooting.md`.

6. **Arquivamento de Spec**:
   - Caso a tarefa pertença a uma spec ativa, mova o diretório de `specs/active/<feature-name>` para `specs/completed/<feature-name>`.
