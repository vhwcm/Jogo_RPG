# ADR 0004: Interface Web Glassmorphic e Backend FastAPI

* **Status**: Aceito
* **Data**: 2026-08-15
* **Autor**: Antigravity AI & Usuário

## 📋 Contexto

A antiga interface gráfica usava Pygame com posições absolutas e elementos visuais fixos. O usuário desejava migrar para uma interface gráfica de alto nível visual, responsiva, com visual medieval luxuoso e desacoplada do terminal.

## 🎯 Decisão

1. Construir uma **Web Application moderna (HTML5, Vanilla CSS3, Javascript ES6)** com estática em **Glassmorphism**, brilhos ambientais, fontes do Google Fonts (*Cinzel* para títulos nobres e *Inter* para o corpo de texto) e animações suaves.
2. Criar um servidor backend em **FastAPI** (`server/app.py`) fornecendo endpoints REST e servindo os arquivos estáticos da interface web.

## ⚡ Consequências

- **Positivas**:
  - Aparência visual surpreendente com modo escuro medieval e efeitos translúcidos.
  - Totalmente responsivo para diferentes tamanhos de tela.
  - Sem necessidade de compiladores nativos complexos ou janelas de Pygame com gambiarras de coordenadas.
- **Negativas**:
  - Requer o servidor HTTP FastAPI em execução (facilitado pelo script `run.py web`).
