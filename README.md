# 🎮 Mini Games - RPG com Google Gemini

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Pro-green.svg)](https://ai.google.dev)
[![Pygame](https://img.shields.io/badge/Pygame-CE%202.5.5-red.svg)](https://pyga.me)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Dois jogos RPG de estratégia desenvolvidos com inteligência artificial usando Google Gemini AI**

## 📋 Índice

- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🚀 Início Rápido](#-início-rápido)
- [⚙️ Configuração Completa](#️-configuração-completa)
- [🎮 Como Jogar](#-como-jogar)
- [🔧 Funcionalidades](#-funcionalidades)
- [💻 Compatibilidade](#-compatibilidade)
- [🐛 Solução de Problemas](#-solução-de-problemas)
- [📚 Documentação](#-documentação)
- [🤝 Contribuindo](#-contribuindo)

---

## 📁 Estrutura do Projeto

```
mini_games/
├── 🎯 rpg_com_gemini/
│   ├── 🖥️ rpg_terminal/          # Versão para terminal
│   │   ├── rpg.py               # Jogo principal
│   │   ├── mundos/              # Salvamentos automáticos
│   │   └── README.md            # Documentação específica
│   └── 🎨 rpg_grafico/          # Versão gráfica
│       ├── rpg_grafico.py       # Jogo principal
│       ├── aventuras/           # Salvamentos (criado automaticamente)
│       ├── lideres/             # 🖼️ Imagens dos líderes (19 espécies)
│       ├── reinos/              # 🏰 Imagens dos reinos
│       ├── musicas/             # 🎵 Efeitos sonoros
│       ├── Cinzel/              # 🔤 Fontes personalizadas
│       └── README.md            # Documentação específica
├── 🐍 venv/                     # Ambiente virtual Python
├── 📄 CONFIGURACAO_AMBIENTE.md  # Guia de configuração detalhado
├── 📄 MUDANCAS_TECNICAS.md      # Log de mudanças técnicas
├── 📄 MODELOS_GEMINI.md         # Informações sobre modelos AI
├── 🔧 setup.sh                 # Script de configuração automática
├── 🔍 verificar_config.sh      # Script de verificação
├── 🎮 executar_jogos.sh        # Menu para executar jogos
└── 📄 README.md                # Este arquivo
```

---

## 🚀 Início Rápido

### 1️⃣ **Configuração Automática**
```bash
# Clone o repositório
git clone https://github.com/vhwcm/mini_games.git
cd mini_games

# Execute a configuração automática
chmod +x setup.sh
./setup.sh
```

### 2️⃣ **Obter Chave API**
1. 🌐 Acesse: **[Google AI Studio](https://aistudio.google.com)**
2. 🔑 Crie uma conta e obtenha chave API **gratuita**
3. 📝 Configure nos arquivos Python (veja seção [Configuração](#️-configuração-completa))

### 3️⃣ **Executar Jogos**
```bash
# Verificar se tudo está OK
./verificar_config.sh

# Jogar
./executar_jogos.sh
```

---

## ⚙️ Configuração Completa

### 🔧 **Dependências do Sistema**

<details>
<summary><strong>🐧 Ubuntu/Debian</strong></summary>

```bash
# Atualizar sistema
sudo apt update

# Dependências básicas
sudo apt install python3 python3-pip python3-venv python3-full -y

# Para RPG Gráfico (pygame dependencies)
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev \
                 libsdl2-mixer-dev libsdl2-ttf-dev -y
```
</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependências
brew install python
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
```
</details>

<details>
<summary><strong>🪟 Windows</strong></summary>

1. 📥 Baixe Python em: [python.org/downloads](https://python.org/downloads)
2. ✅ Durante instalação, marque **"Add Python to PATH"**
3. 🔄 Reinicie o computador
4. ▶️ Execute scripts no **PowerShell** ou **CMD**
</details>

### 🐍 **Ambiente Virtual Python**

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 📦 **Dependências Python**

> ⚠️ **IMPORTANTE:** Use `pygame-ce` em vez de `pygame` padrão!

```bash
# Ativar ambiente virtual primeiro
source venv/bin/activate

# Instalar dependências principais
pip install google-generativeai

# Para RPG Gráfico - usar pygame-ce (Community Edition)
pip install pygame-ce pygame_gui

# Verificar instalação
pip list | grep -E "(google|pygame)"
```

### 🔑 **Configuração da API Google Gemini**

#### **Obter Chave API:**
1. 🌐 Acesse: **[Google AI Studio](https://aistudio.google.com)**
2. 🔐 Faça login com sua conta Google
3. ➕ Clique em **"Get API Key"** → **"Create API Key"**
4. 📋 Copie a chave gerada (formato: `AIzaSyA...`)

#### **Configurar nos Arquivos:**

**🖥️ RPG Terminal** (`rpg_com_gemini/rpg_terminal/rpg.py`, linha 12):
```python
API_KEY = 'SUA_CHAVE_AQUI'  # 👈 Substitua pela sua chave real
```

**🎨 RPG Gráfico** (`rpg_com_gemini/rpg_grafico/rpg_grafico.py`, linha 16):
```python
API_KEY = 'SUA_CHAVE_AQUI'  # 👈 Substitua pela sua chave real
```

---

## 🎮 Como Jogar

### 🖥️ **RPG Terminal**
```bash
cd rpg_com_gemini/rpg_terminal
source ../../venv/bin/activate
python3 rpg.py
```

**Características:**
- 📝 Interface baseada em texto
- 🌟 **Qualquer espécie/raça** que você imaginar
- 💾 Salvamento automático em `mundos/`
- 👥 Sistema multiplayer básico (mesmo arquivo)
- ⏰ Digite **"fim"** para sair

### 🎨 **RPG Gráfico**
```bash
cd rpg_com_gemini/rpg_grafico  
source ../../venv/bin/activate
python3 rpg_grafico.py
```

**Características:**
- 🖼️ Interface visual com pygame
- 👑 **19 espécies predefinidas** com avatares únicos
- 💾 Salvamento em `aventuras/`
- 🎵 Recursos visuais e sonoros
- 🖱️ Controle por mouse e teclado

---

## 🔧 Funcionalidades

### 🏰 **Sistema de Reino**

| Status | Faixa | Descrição |
|--------|-------|-----------|
| 😊 **Felicidade** | 0-100% | Satisfação dos cidadãos |
| ⚔️ **Poder Militar** | 0-100,000 | Força do exército |
| 🛐 **Religião** | Variável | Fé do reino (únicas no jogo) |
| 💰 **Dinheiro** | 0-100,000 | Recursos econômicos |
| 👑 **Nome do Reino** | Customizável | Sua criação |

### 🎯 **Jogabilidade**

- 📊 **Decisões Estratégicas:** Econômicas, religiosas, militares
- 🤝 **Sistema Diplomático:** Forme aliados ou declare guerras  
- 🧠 **Quizzes e Desafios:** Teste sua estratégia
- 🔢 **Opções Numeradas:** Interface amigável
- 📖 **Contexto Persistente:** História mantida durante sessões
- 💾 **Continuidade:** Retomar aventuras salvas

### 🎭 **Espécies Disponíveis (RPG Gráfico)**

<details>
<summary><strong>👥 Humanoides (7 espécies)</strong></summary>

- 🏔️ **Anão** - Mestres da forja e mineração
- 🐎 **Centauro** - Guerreiros das planícies  
- 🧝 **Elfo** - Sábios da floresta
- 🐐 **Fauno** - Guardiões da natureza
- 🏠 **Gnomo** - Inventores engenhosos
- 👤 **Humano** - Versáteis e adaptáveis
- 🍀 **Leprechaun** - Sortudos e travessos
</details>

<details>
<summary><strong>🔮 Místicos (5 espécies)</strong></summary>

- 👹 **Demônio** - Senhores das chamas
- 🧞 **Djinn** - Mestres dos desejos
- 🌪️ **Elemental** - Forças da natureza
- 🧙 **Mago** - Estudiosos das artes arcanas
- 🧛 **Vampiro** - Imortais da noite
</details>

<details>
<summary><strong>🐲 Bestiais (5 espécies)</strong></summary>

- 🐉 **Dragão** - Majestosos e poderosos
- 👹 **Goblin** - Pequenos mas espertos
- ⚔️ **Orc** - Guerreiros ferozes
- 🦏 **Rinoceronte** - Força bruta
- 🌉 **Trol** - Guardiões das pontes
</details>

<details>
<summary><strong>🌊 Aquáticos & Místicos (2 espécies)</strong></summary>

- 🧜 **Sereia** - Rainhas dos oceanos
- ☠️ **Morto-vivo** - Eternos e resilientes
</details>

---

## 💻 Compatibilidade

| Sistema | 🖥️ RPG Terminal | 🎨 RPG Gráfico | 📝 Observações |
|---------|----------------|----------------|-----------------|
| 🐧 **Linux (Ubuntu)** | ✅ Perfeito | ✅ Funciona | Requer deps SDL |
| 🐧 **WSL** | ✅ Perfeito | ⚠️ Limitado | Problemas gráficos possíveis |
| 🍎 **macOS** | ✅ Perfeito | ✅ Funciona | Requer Homebrew |
| 🪟 **Windows** | ✅ Perfeito | ✅ **Recomendado** | Melhor performance |

### 🔧 **Requisitos Mínimos**

- 🐍 **Python:** 3.8+
- 💾 **RAM:** 4GB (recomendado: 8GB)
- 🌐 **Internet:** Para API Gemini
- 🎮 **Gráfico:** Qualquer (OpenGL básico)

---

## 🐛 Solução de Problemas

<details>
<summary><strong>❌ Erro: cannot import name 'DIRECTION_LTR' from 'pygame'</strong></summary>

**Causa:** Conflito entre `pygame` e `pygame_gui`

**Solução:**
```bash
pip uninstall pygame pygame-ce pygame_gui -y
pip install pygame-ce pygame_gui
```
</details>

<details>
<summary><strong>❌ Erro: 404 models/gemini-1.5-pro-latest not found</strong></summary>

**Causa:** Modelo Gemini desatualizado

**Solução:** Código já atualizado para `gemini-2.5-pro` ✅
</details>

<details>
<summary><strong>❌ Erro: API key not configured</strong></summary>

**Causa:** Chave API não configurada

**Solução:**
1. Obter chave em: [aistudio.google.com](https://aistudio.google.com)
2. Configurar nos arquivos Python
3. Verificar se não há espaços extras
</details>

<details>
<summary><strong>❌ Erro: Surface is not initialized (Linux/WSL)</strong></summary>

**Causa:** Sem display gráfico disponível

**Soluções:**
- Use RPG Terminal se não há interface gráfica
- Configure X11 forwarding para SSH: `export DISPLAY=:0`
- Use Windows diretamente se estiver no WSL
</details>

### 🆘 **Comandos de Diagnóstico**

```bash
# Verificar configuração completa
./verificar_config.sh

# Testar dependências Python
python3 -c "
import google.generativeai as genai
import pygame
import pygame_gui
print('✅ Todas as dependências OK')
"

# Testar API Gemini
python3 -c "
import google.generativeai as genai
genai.configure(api_key='SUA_CHAVE_AQUI')
model = genai.GenerativeModel('gemini-2.5-pro')
response = model.generate_content('Teste')
print('✅ API Gemini funcionando!')
"
```

---

## 📚 Documentação

### 📄 **Arquivos de Documentação**

- 📋 **[CONFIGURACAO_AMBIENTE.md](CONFIGURACAO_AMBIENTE.md)** - Guia detalhado de configuração
- 🔧 **[MUDANCAS_TECNICAS.md](MUDANCAS_TECNICAS.md)** - Log completo de mudanças
- 🤖 **[MODELOS_GEMINI.md](MODELOS_GEMINI.md)** - Informações sobre modelos AI
- 🖥️ **[rpg_terminal/README.md](rpg_com_gemini/rpg_terminal/README.md)** - Documentação específica
- 🎨 **[rpg_grafico/README.md](rpg_com_gemini/rpg_grafico/README.md)** - Documentação específica

### 🔗 **Links Úteis**

- 🔑 **[Google AI Studio](https://aistudio.google.com)** - Obter chave API
- 📖 **[Documentação Gemini](https://ai.google.dev/)** - Referência oficial
- 🎮 **[Pygame-CE](https://pyga.me/)** - Biblioteca gráfica
- 🎨 **[Pygame GUI](https://pygame-gui.readthedocs.io/)** - Interface gráfica

---

## 🤝 Contribuindo

### 🚀 **Como Contribuir**

1. 🍴 **Fork** o repositório
2. 🌟 **Clone** sua fork localmente
3. 🔧 **Configure** o ambiente de desenvolvimento
4. ✨ **Faça** suas melhorias
5. 🧪 **Teste** suas mudanças
6. 📤 **Envie** um Pull Request

### 💡 **Ideias para Contribuições**

- 🆕 **Novas espécies** para o RPG gráfico
- 🎵 **Efeitos sonoros** adicionais
- 🌍 **Tradução** para outros idiomas
- 🐛 **Correções de bugs**
- 📚 **Melhorias na documentação**
- ⚡ **Otimizações de performance**

### 📝 **Diretrizes**

- Siga o padrão de código existente
- Adicione testes quando aplicável
- Atualize a documentação conforme necessário
- Use commits descritivos

---

## ⭐ **Status do Projeto**

| Componente | Status | Versão |
|------------|--------|--------|
| 🖥️ **RPG Terminal** | ✅ Estável | v2.0 |
| 🎨 **RPG Gráfico** | ✅ Estável | v2.0 |
| 🤖 **Gemini AI** | ✅ Funcional | 2.5-pro |
| 📚 **Documentação** | ✅ Completa | - |

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🎉 Conclusão

**Mini Games RPG** oferece uma experiência única de RPG de estratégia alimentada por IA, com duas modalidades distintas para diferentes preferências de jogabilidade.

### ✨ **Destaques:**

- 🤖 **IA Avançada:** Powered by Google Gemini 2.5 Pro
- 🎮 **Duas Versões:** Terminal e Gráfica
- 🏰 **Estratégia Profunda:** Sistema complexo de reino
- 💾 **Persistência:** Salva e continua aventuras
- 🌟 **Customização:** Espécies variadas e criativas

---

<div align="center">

**🎭 Torne-se o governante que seu reino merece! 👑**

[🚀 Começar Agora](#-início-rápido) • [📚 Documentação](#-documentação) • [🐛 Reportar Bug](https://github.com/vhwcm/mini_games/issues) • [💡 Sugerir Feature](https://github.com/vhwcm/mini_games/issues)

---

*Desenvolvido com ❤️ usando Google Gemini AI*

[![GitHub stars](https://img.shields.io/github/stars/vhwcm/mini_games?style=social)](https://github.com/vhwcm/mini_games/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/vhwcm/mini_games?style=social)](https://github.com/vhwcm/mini_games/network/members)

</div>
