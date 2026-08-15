# ADR 0001: Arquitetura em Camadas Decoplada (CLI & Web)

* **Status**: Aceito
* **Data**: 2026-08-15
* **Autor**: Antigravity AI & Usuário

## 📋 Contexto

O projeto original possuía duas versões independentes do jogo (`terminal_rpg/rpg.py` e `ui_rpg/rpg_grafico.py`), com código duplicado, posições absolutas hardcoded no Pygame e falta de abstração das regras do jogo. Mudanças na lógica precisavam ser replicadas manualmente em ambos os arquivos.

## 🎯 Decisão

Adotou-se uma **Arquitetura em Camadas Decoplada (Clean Architecture / Hexagonal)**:
- Todo o motor do jogo ressurge no módulo central `engine/`, contendo a lógica de domínio (`engine/domain/`), persistência (`engine/db/`), memória (`engine/memory/`) e provedores de IA (`engine/providers/`).
- As interfaces de usuário (**CLI Terminal** com `rich` e **Web Application** com `FastAPI` + `HTML5/CSS3/JS`) passam a ser simples clientes que consomem a mesma `GameEngine`.

## ⚡ Consequências

- **Positivas**:
  - Eliminação de duplicidade de código de jogo.
  - Possibilidade de adicionar novas UIs (ex: bot de Discord, aplicativo mobile) sem alterar o motor.
  - Testabilidade independente das regras de jogo.
- **Negativas**:
  - Requer maior estrutura inicial de pastas e DTOs de comunicação.
