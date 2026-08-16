# Guia de Padrões e Boas Práticas para Diagramas D2

Este guia define as convenções para criação e manutenção dos diagramas arquiteturais e de fluxo utilizando a linguagem declarativa **D2** no repositório **AI RPG Game**.

---

## 1. Por que D2?
- **Declarativo & Versionável**: Arquivos `.d2` são texto puro, permitindo diffs claros no Git e manutenção direta por agentes de IA e desenvolvedores.
- **Autoexplicativo**: Os diagramas D2 devem fornecer compreensão imediata da estrutura, limites e fluxos do sistema sem necessidade de ler código-fonte.
- **Consistência Visual**: Suporta layouts automáticos, containers aninhados, estilização de conexões e rotulação semântica.

---

## 2. Estrutura e Localização dos Diagramas

Os diagramas D2 devem ser organizados em:
- `docs/diagrams/`: Diagramas de visão macro, arquitetura geral, infraestrutura e subsistemas transversais.
- `docs/diagrams/<subsystem>.d2`: Diagramas específicos de fluxos ou sistemas.
- `specs/active/<feature>/`: Diagramas de design específicos da funcionalidade em desenvolvimento (movidos para `specs/completed/` no arquivamento).

Todos os diagramas D2 devem ser referenciados em formato de bloco de código `d2` ou link correspondente nos documentos Markdown (`docs/architecture/`, `docs/systems/`, `docs/decisions/`).

---

## 3. Padrões de Estilo e Nomenclatura

### Nomes de Nós e Containers
- Use nomes semânticos em camelCase ou snake_case para identificadores de nós e títulos claros para labels:
  ```d2
  presentation: Presentation Layer {
    webSpa: Web SPA (Vanilla JS/CSS)
    cli: Rich CLI Interface
  }
  ```

### Conexões e Direcionamento
- Indique o sentido do fluxo de dados ou invocação através de setas (`->`, `<->`).
- Rotule conexões com o protocolo ou tipo de dado trafegado:
  ```d2
  webSpa -> serverApi: HTTP REST / JSON DTOs
  serverApi -> gameEngine: Calls domain methods
  ```

### Cores e Estilização
- Utilize containers para representar camadas arquiteturais (Clean Architecture).
- Mantenha contrastes legíveis e padronizados para componentes internos e externos:
  ```d2
  externalProviders: External AI Providers {
    style.stroke-dash: 3
    gemini: Google Gemini API
    groq: Groq Cloud API
  }
  ```

---

## 4. Checklist de Criação e Atualização de Diagramas D2

Sempre que implementar ou modificar um componente:
1. **Verificar Diagramas Existentes**: Inspecione `docs/diagrams/` e identifique se o fluxo ou componente já existe.
2. **Atualizar Nós e Conexões**: Se a assinatura, contrato ou caminho de dados mudou, ajuste os nós correspondentes.
3. **Validar Clareza**: O diagrama deve responder com clareza:
   - *O que este subsistema faz?*
   - *Quais componentes conversam entre si?*
   - *Qual é o caminho dos dados e onde ocorrem transformações?*
   - *Onde ocorrem fallbacks ou tratamentos de erro?*
