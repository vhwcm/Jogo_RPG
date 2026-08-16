# ADR-001: Arquitetura em Camadas Desacoplada (Clean Architecture)

* **Status**: Aceito
* **Data**: 2026-08-15
* **Decisores**: Equipe de Desenvolvimento AI RPG

## Contexto
O projeto original possuía versões independentes do jogo com lógica de regras misturada a loops de renderização do Pygame e scripts de terminal, gerando duplicação de regras de negócio e dificuldade para introduzir novas interfaces.

## Decisão
Adotar uma **Clean Layered Architecture (Arquitetura Hexagonal)**:
- Todo o motor do jogo reside no módulo `engine/`, encapsulando domínio (`engine/domain/`), persistência (`engine/db/`), memória (`engine/memory/`) e provedores de IA (`engine/providers/`).
- As interfaces de usuário (CLI Terminal e Web SPA) são apenas clientes que interagem através da `GameEngine` ou de DTOs REST no `server/`.

## Alternativas Consideradas
- **Monolito com Pygame**: Rápido para prototipagem simples, mas inviável para evolução web responsiva e testes automatizados.
- **Microserviços com gRPC**: Complexidade desnecessária para execução local e portátil de um jogo single-player.

## Consequências
- **Positivas**:
  - Eliminação de duplicidade de lógica.
  - Testabilidade isolada de cada camada (domínio, repositório, provedores).
  - Portabilidade total para novas interfaces de usuário.
- **Negativas**:
  - Exige criação de contratos formais de dados (DTOs) e mapeamento entre camadas.
