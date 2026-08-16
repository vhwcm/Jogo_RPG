# ADR-004: Interface Web Glassmorphism e API REST FastAPI

* **Status**: Aceito
* **Data**: 2026-08-15
* **Decisores**: Equipe de Desenvolvimento AI RPG

## Contexto
O jogo necessitava de uma apresentação visual imersiva, moderna e responsiva, abandonando as limitações de telas de terminais e janelas estáticas de Pygame.

## Decisão
1. Construir uma **Web Application SPA** em Vanilla HTML5/CSS3/JavaScript com design **Glassmorphism**, tipografia nobre (`Cinzel`) e áudio adaptativo reativo ao humor narrativo (`clima`).
2. Criar a camada de transporte em **FastAPI** (`server/app.py`), servindo simultaneamente a API REST e os arquivos estáticos.

## Alternativas Consideradas
- **React / Next.js**: Introduziria etapa de build (Node.js/npm) desnecessária para uma interface focada em gameplay narrativo e mapa tático.
- **Pygame / Tkinter**: Falta de responsividade moderna, tipografia refinada e animações fluidas de CSS.

## Consequências
- **Positivas**:
  - Zero etapa de build para o frontend; alterações em JS/CSS refletem instantaneamente.
  - Aparência visual premium e imersiva.
  - Rápida integração com o backend FastAPI.
- **Negativas**:
  - Requer que o servidor FastAPI esteja em execução para carregar a interface web.
