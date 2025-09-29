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

## 🛠️ Scripts Utilitários

### 🔧 **setup.sh - Configuração Automática**

Script completo que configura todo o ambiente automaticamente:

```bash
chmod +x setup.sh
./setup.sh
```

**✨ O que o script faz:**
- ✅ Verifica se Python 3.8+ está instalado
- ✅ Cria ambiente virtual Python
- ✅ Instala todas as dependências necessárias
- ✅ Verifica se tudo foi instalado corretamente
- ✅ Cria pastas necessárias (`mundos/`)
- ✅ Fornece instruções para próximos passos

### 🎮 **executar_jogos.sh - Menu de Execução**

Launcher interativo para facilitar a execução dos jogos:

```bash
chmod +x executar_jogos.sh
./executar_jogos.sh
```

**🎯 Opções disponíveis:**
1. 🖥️ **RPG Terminal** - Versão texto
2. 🎮 **RPG Gráfico** - Versão visual
3. 🔍 **Verificar configuração**
4. ❌ **Sair**

**💡 Funcionalidades:**
- ✅ Ativa automaticamente o ambiente virtual
- ✅ Verifica problemas gráficos (WSL/SSH)
- ✅ Navega para o diretório correto
- ✅ Fornece avisos sobre configuração da API

### 🔍 **verificar_config.sh - Diagnóstico Completo**

Script de diagnóstico que verifica toda a configuração:

```bash
chmod +x verificar_config.sh
./verificar_config.sh
```

**🔎 Verificações realizadas:**
- ✅ **Python:** Versão e disponibilidade
- ✅ **Ambiente Virtual:** Existência e ativação
- ✅ **Dependências:** Google Generative AI, Pygame-CE, Pygame GUI
- ✅ **Arquivos:** Estrutura do projeto e códigos principais
- ✅ **Recursos:** Imagens, músicas, fontes (RPG Gráfico)
- ✅ **API:** Configuração das chaves nos códigos
- ✅ **Sistema Gráfico:** Compatibilidade para RPG Gráfico
- ✅ **Conectividade:** Acesso à internet

**📊 Relatório final:**
- 🎉 Se tudo OK: "Configuração perfeita!"
- ⚠️ Se problemas: Lista soluções específicas

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