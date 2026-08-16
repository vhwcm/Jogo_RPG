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

2. **Mapeamento Arquitetural**:
   - Inspecione `docs/architecture/overview.md` e os documentos especializados (`backend.md`, `frontend.md`, `database.md`, `infrastructure.md`).
   - Identifique quais camadas serão tocadas pela demanda (Apresentação, API, Domínio, Memória, Banco ou Provedores).

3. **Consulta aos Modelos de Domínio e Sistemas**:
   - Consulte `docs/domain/` para compreender entidades, métricas de estado do reino e contratos de dados.
   - Consulte `docs/systems/` para entender o ciclo de vida dos processos envolvidos (ex: `turn_execution.md`).

4. **Verificação de Decisões Prévias (ADRs)**:
   - Consulte `docs/decisions/` para entender por que as tecnologias e padrões atuais foram escolhidos e quais alternativas foram rejeitadas.

5. **Localização e Análise do Código Relacionado**:
   - Localize as classes, arquivos e testes relevantes usando ferramentas de busca de código (`rg`, `fd`).
   - Avalie as assinaturas de métodos e fluxos de dados reais.

6. **Síntese de Contexto**:
   - Estruture um resumo mental ou compartilhado com o usuário destacando:
     - Componentes afetados.
     - Padrões arquiteturais a preservar.
     - Potenciais riscos ou restrições identificadas.
