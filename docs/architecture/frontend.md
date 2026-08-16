# 🎨 Frontend Architecture (Web SPA)

## 1. Visão Geral
A interface web do **AI RPG Game** é uma Single Page Application (SPA) moderna, rápida e leve, construída sem frameworks pesados (Vanilla JavaScript ES6+, HTML5 semântico e CSS3 puro).

---

## 2. Estrutura de Arquivos

```
web/
├── index.html          — Estrutura semântica principal e templates
├── css/
│   ├── main.css        — Tokens CSS globais, Glassmorphism, reset, layouts e breakpoints
│   └── components.css  — Estilos específicos de componentes (cards, botões, modais, painéis)
├── js/
│   ├── app.js          — Ponto de entrada, inicialização de listeners e ciclo de vida da UI
│   ├── ui.js           — Manipulação de DOM, renderização de cards, status e decisões
│   ├── audio.js        — Web Audio Manager e transições dinâmicas de trilha sonora
│   └── tactical_map.js — Renderização e interação com o mapa tático do reino
└── assets/
    ├── lideres/        — Retratos dos líderes de cada raça
    ├── reinos/         — Imagens temáticas dos reinos
    └── musicas/        — Trilhas sonoras para cada clima emocional
```

---

## 3. Padrão Visual (Glassmorphism & Design Tokens)

- **Tema Visual**: Fantasia medieval imersiva com efeitos de vidro fosco (`backdrop-filter: blur(12px)`), tipografia serifada majestosa (`Cinzel`) e paletas com contraste balanceado.
- **Micro-interações**: Feedback visual instantâneo para botões, seleção de opções e transições suaves de turnos.
- **Responsividade**: Layouts fluidos adaptáveis a desktops, tablets e smartphones sem quebra de viewport.

---

## 4. Gerenciamento de Áudio Dinâmico (`web/js/audio.js`)

O sistema reage ao atributo `clima` retornado pelo Game Master em cada turno:

| Clima Retornado | Arquivo de Áudio | Propósito Atmosférico |
|---|---|---|
| `aventura` | `clima de aventura.mp3` | Exploração, novas descobertas e viagens |
| `calmo` | `clima de calmo.mp3` | Momentos de paz, audiências cotidianas |
| `desenvolvimento` | `clima de desenvolvimento.mp3` | Construção, reformas e expansão econômica |
| `frenetico` | `clima frenetico.mp3` | Batalhas, invasões iminentes e crises |
| `desespero` | `clima de desespero.mp3` | Derrotas, pestes, revoltas ou perdas críticas |
| `harmonia` | `clima de harmonia.mp3` | Festivais, alianças bem-sucedidas e celebrações |

O `AudioManager` implementa cross-fading suave entre faixas, controle de volume persistido em `localStorage` e respeito a restrições de autoplay de navegadores.
