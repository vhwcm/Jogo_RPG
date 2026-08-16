# 🌐 Módulo Web (`web`)

O módulo `web` é a interface de usuário moderna (SPA - Single Page Application) do **AI RPG Game**, construída com HTML5 semântico, Vanilla JavaScript modular e Vanilla CSS avançado com design em Glassmorphism e tema medieval escuro.

---

## 📂 Estrutura do Módulo

```
web/
├── assets/
│   ├── lideres/    # Retratos e ilustrações dos líderes de cada raça
│   ├── musicas/    # Trilhas sonoras temáticas adaptativas por clima
│   └── reinos/     # Panoramas visuais dos castelos e reinos de cada raça
├── css/
│   ├── main.css        # Layout base, design system, paleta de cores e variáveis CSS
│   └── components.css  # Componentes de UI: drawers, cards, badges, modais e botões
├── js/
│   ├── app.js      # Controlador principal, comunicação com a API REST e fluxo de jogo
│   ├── ui.js       # Manipulação de DOM, renderização de crônicas, cards e animações
│   └── audio.js    # Gerenciador de áudio adaptativo e transição de trilhas por clima
└── index.html      # Página única da aplicação
```

---

## ✨ Principais Funcionalidades da Interface Web

1. **Painel de Status em Tempo Real**: Indicadores visuais de Ouro, População, Exército, Felicidade, Religião e Soberano com efeitos de brilho e animações de transição.
2. **Crônica Real Interativa**: Renderização da narrativa gerada pela IA, com opções de decisão clicáveis e botões para estimar impactos antes de confirmar uma escolha.
3. **Trilha Sonora Adaptativa (`audio.js`)**: Troca suave de faixas de áudio sincronizadas com o clima emocional retornado pelo Game Master:
   - `clima de aventura`
   - `clima de calmo`
   - `clima frenetico`
   - `clima de harmonia`
   - `clima de desenvolvimento`
   - `clima de desespero`
4. **Drawers Laterais de Gestão**:
   - **Reino & Ativos**: Visualização em cards de construções, fortificações, postos avançados, santuários e itens.
   - **Diplomacia**: Lista de impérios vizinhos com barras de afinidade, poderio militar e status de aliança/guerra.
   - **Aventuras (Campanhas)**: Gerenciador de múltiplos saves, criação de novas campanhas, exclusão e histórico de turnos.
5. **Importação e Exportação de Saves**: Permite baixar o save completo da campanha em JSON ou carregar um arquivo previamente exportado.

---

## 🚀 Como Visualizar

Inicie o servidor backend para servir a pasta estática:
```bash
python run.py --web
```
Em seguida, abra o navegador em `http://localhost:8000`.
