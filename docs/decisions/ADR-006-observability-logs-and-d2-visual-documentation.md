# ADR-006: Observabilidade Transversal com Logs Estruturados e Documentação Visual Viva com D2

* **Status**: Aceito
* **Data**: 2026-08-16
* **Decisores**: Equipe de Desenvolvimento AI RPG & Agentes Autônomos

## Contexto
O sistema AI RPG Game opera com múltiplos subsistemas interconectados (FastAPI, SQLite3, Vector Store, LLM Providers com fallback dinâmico, GameEngine de simulação de estado). Diagnosticar falhas de runtime e inconsistências em fluxos complexos apenas lendo código é custoso e passível de premissas incorretas. Além disso, a rápida evolução da arquitetura e das regras de domínio exige uma documentação visual clara, concisa e manutenível que permita a desenvolvedores e agentes compreenderem a topologia e o fluxo de dados sem necessidade de decodificar o código-fonte.

## Decisão

### 1. Sistema de Observabilidade e Logs Estruturados
1. **Instrumentação Obrigatória**: Toda funcionalidade relevante deve emitir logs nos seus pontos críticos de execução (início/fim de operações, tomadas de decisão, transições de estado, chamadas de inferência de IA, erros e rollbacks).
2. **Contextualização Estruturada**: Os logs devem conter metadados suficientes (`campaign_id`, `turn_number`, `action_type`, `provider`, `duration_ms`, `error_type`) para reconstituir o histórico do evento.
3. **Níveis Semânticos de Log**:
   - `DEBUG`: Detalhes finos de execução e sanitização de payloads.
   - `INFO`: Marcos de ciclo de vida e transições bem-sucedidas.
   - `WARNING`: Falhas toleradas, acionamento de fallback de LLM, anomalias recuperáveis.
   - `ERROR`: Falhas de operação com stack trace e contexto.
   - `CRITICAL`: Violações de integridade estrutural irrecuperáveis.
4. **Segurança Rigorosa**: Chaves de API (`GEMINI_API_KEY`, `GROQ_API_KEY`, etc.), senhas e tokens nunca devem ser registrados nos logs.
5. **Troubleshooting Orientado a Evidências**: Agentes e desenvolvedores devem inspecionar logs reais de execução durante o diagnóstico de problemas em vez de presumir hipóteses.
6. **Procedimentos Reutilizáveis**: Documentar procedimentos recorrentes de troubleshooting em `docs/guides/observability_and_troubleshooting.md`.

### 2. Padrão D2 para Documentação Visual
1. **Adoção do D2**: D2 é adotado como a linguagem padrão declarativa para diagramas de arquitetura, fluxo de dados, sequência e interações entre componentes.
2. **Gatilho de Criação e Atualização**: Qualquer alteração em fluxos de dados, componentes, processos assíncronos, regras de negócio ou decisões arquiteturais exige a criação ou atualização do respectivo diagrama D2.
3. **Armazenamento e Referência**: Os arquivos `.d2` são armazenados em `docs/diagrams/` e referenciados diretamente nos documentos Markdown, Specs e ADRs.
4. **Independência de Código**: O objetivo dos diagramas D2 é permitir a compreensão completa do subsistema sem depender da leitura direta de código-fonte.

## Alternativas Consideradas
- **Logs Não Estruturados (print/raw strings)**: Difíceis de parsear, ruidosos e carentes de contexto estruturado.
- **Ferramentas Visuais Proprietárias ou Binárias (PNGs soltos)**: Não versionáveis via Git diff, tornando impossível a sincronização contínua por agentes de IA.
- **Mermaid Exclusivo**: Menor expressividade visual, menor controle de layout e limitações para diagramas de arquitetura complexos em comparação ao D2.

## Consequências
- **Positivas**:
  - Diagnóstico imediato de falhas de runtime através de evidências concretas de log.
  - Redução drástica da carga cognitiva para entender a arquitetura do projeto.
  - Documentação visual viva, versionada no Git e mantida sincronizada a cada spec/feature.
  - Proteção absoluta contra vazamento de credenciais nos logs.
- **Negativas**:
  - Exige disciplina contínua na instrumentação de logs e na sincronização dos diagramas D2 em cada alteração de escopo.
