---
name: explore-project
description: Explora e compreende a arquitetura, modelos de domínio, ADRs e código existente antes de propor ou iniciar qualquer alteração no projeto.
---

# Skill: explore-project

## Objetivo
Garantir que o agente construa um modelo mental preciso do projeto antes de escrever código ou propor especificações, evitando premissas errôneas ou quebra de padrões arquiteturais existentes.

## Quando Utilizar
- Ao iniciar uma nova feature ou sistema.
- Ao investigar bugs complexos ou comportamentos inesperados.
- Ao receber uma solicitação com impacto arquitetural ou estrutural.

## Fluxo de Execução

1. **Leitura das Instruções Centrais**:
   - Inspecione `AGENTS.md` e os arquivos em `.agent/rules/`.

2. **Mapeamento Arquitetural & Visual (D2)**:
   - Inspecione `docs/architecture/overview.md`, os documentos especializados (`backend.md`, `frontend.md`, `database.md`, `infrastructure.md`) e os diagramas D2 em `docs/diagrams/` para obter um entendimento visual rápido sem precisar ler código.
   - Identifique quais camadas serão tocadas pela demanda (Apresentação, API, Domínio, Memória, Banco ou Provedores).

3. **Consulta aos Modelos de Domínio e Sistemas**:
   - Consulte `docs/domain/` para compreender entidades, métricas de estado do reino e contratos de dados.
   - Consulte `docs/systems/` e seus diagramas de fluxo D2 para entender o ciclo de vida dos processos envolvidos (ex: `turn_execution.md`).

4. **Verificação de Decisões Prévias (ADRs)**:
   - Consulte `docs/decisions/` para entender por que as tecnologias e padrões atuais foram escolhidos e quais alternativas foram rejeitadas.

5. **Localização, Análise de Código e Evidências de Logs**:
   - Localize as classes, arquivos e testes relevantes usando ferramentas de busca de código (`rg`, `fd`).
   - Avalie as assinaturas de métodos e fluxos de dados reais.
   - Em caso de investigação de falhas ou bugs, inspecione os logs estruturados emitidos pelo sistema e consulte os procedimentos em `docs/guides/observability_and_troubleshooting.md`.

6. **Síntese de Contexto**:
   - Estruture um resumo mental ou compartilhado com o usuário destacando:
     - Componentes afetados e diagramas D2 relacionados.
     - Padrões arquiteturais a preservar.
     - Pontos de observabilidade a instrumentar ou verificar.
     - Potenciais riscos ou restrições identificadas.

