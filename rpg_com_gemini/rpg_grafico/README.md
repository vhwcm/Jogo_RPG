# 🎮 RPG Gráfico - Aventura Visual com IA

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/Pygame--CE-2.5.5-red.svg)](https://pyga.me)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Pro-green.svg)](https://ai.google.dev)
[![GUI](https://img.shields.io/badge/Interface-Visual-purple.svg)](#)

> **RPG de aventura com interface gráfica, powered by Google Gemini AI**

---

## 📋 Índice

- [🚀 Execução Rápida](#-execução-rápida)
- [⚙️ Configuração](#️-configuração)
- [🎮 Como Jogar](#-como-jogar)
- [🎭 Espécies e Líderes](#-espécies-e-líderes)
- [🖼️ Interface Gráfica](#️-interface-gráfica)
- [🎵 Sistema de Áudio](#-sistema-de-áudio)
- [🛠️ Recursos Visuais](#️-recursos-visuais)
- [🐛 Solução de Problemas](#-solução-de-problemas)
- [🎨 Personalização](#-personalização)

---

## 🚀 Execução Rápida

### 🎯 **Método 1: Scripts Automáticos (Recomendado)**

```bash
# A partir do diretório raiz do projeto
./executar_jogos.sh
# Escolha a opção 2 para RPG Gráfico
```

### 💻 **Método 2: Execução Manual**

```bash
# A partir do diretório raiz do projeto
source venv/bin/activate
cd rpg_com_gemini/rpg_grafico
python3 rpg_grafico.py
```

### 📋 **Pré-requisitos**
- ✅ Ambiente virtual ativado
- ✅ Pygame-CE instalado
- ✅ Pygame GUI configurado
- ✅ Chave API do Gemini
- ✅ Recursos gráficos e sonoros

### 🔧 **Verificar Configuração**

```bash
# Do diretório raiz do projeto
./verificar_config.sh
```

---

## ⚙️ Configuração

### 🔑 **1. Chave API do Google Gemini**

#### **Obter Chave:**
1. 🌐 Acesse: **[Google AI Studio](https://aistudio.google.com)**
2. 🔐 Faça login e crie uma chave API **gratuita**
3. 📋 Copie a chave gerada

#### **Configurar no Código:**
📝 **Edite o arquivo `rpg_grafico.py`, linhas 19-20:**

```python
# Configure sua chave API aqui
genai.configure(api_key='SUA_CHAVE_DE_API_AQUI')  # 👈 Substitua pela sua chave real
```

### 📦 **2. Dependências**

#### **🎯 Configuração Automática (Recomendado):**

```bash
# A partir do diretório raiz do projeto
./setup.sh
```

Este script irá:
- ✅ Verificar Python 3.8+
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Verificar instalação
- ✅ Criar pastas necessárias

#### **⚙️ Configuração Manual:**

```bash
# A partir do diretório raiz do projeto
source venv/bin/activate
pip install pygame-ce pygame_gui google-generativeai
```

### 🎨 **3. Recursos Visuais**

O jogo inclui assets visuais organizados:

```
rpg_grafico/
├── 🖼️ lideres/          # Imagens dos líderes (19 espécies)
├── 🏰 reinos/           # Imagens dos reinos correspondentes
├── 🎵 musicas/          # Trilhas sonoras ambientais
├── ✒️ Cinzel/           # Fonte personalizada
└── 📄 rpg_grafico.py    # Código principal
```

---

## 🎮 Como Jogar

### 🏁 **Iniciando o Jogo**

1. ▶️ **Execute:** `python3 rpg_grafico.py`
2. 🖱️ **Clique** em "Novo Jogo" na tela inicial
3. 🎭 **Escolha** sua espécie na galeria visual
4. 📝 **Digite** seu nome de usuário
5. 🏰 **Digite** o nome do seu reino
6. 🌟 **Comece** sua aventura!

### 🖱️ **Controles**

| Controle | Função |
|----------|--------|
| 🖱️ **Mouse** | Navegação principal |
| ⌨️ **Teclado** | Digitação de texto |
| 🖱️ **Clique** | Seleção de espécies e botões |
| 📝 **Enter** | Enviar mensagens |
| 🔚 **Fechar janela** | Sair do jogo |

### 🎯 **Fluxo do Jogo**

1. **🎭 Seleção de Espécie:** Escolha visual entre 19 opções
2. **📝 Personalização:** Defina nomes únicos
3. **🎮 Aventura:** Interaja com o Gemini AI
4. **🎵 Imersão:** Trilha sonora dinâmica
5. **🏰 Progressão:** Desenvolva seu reino

---

## 🎭 Espécies e Líderes

### 👑 **19 Espécies Disponíveis**

O jogo oferece uma variedade rica de espécies, cada uma com:
- 🖼️ **Imagem única** do líder
- 🏰 **Reino personalizado** correspondente
- 🎨 **Arte exclusiva** de alta qualidade

#### 🌟 **Galeria de Espécies:**

| Categoria | Espécies Disponíveis |
|-----------|---------------------|
| 🏛️ **Clássicas** | Humano, Elfo, Anão, Orc |
| 🐲 **Místicas** | Dragão, Mago, Elemental |
| 😈 **Sombrias** | Demônio, Vampiro, Morto Vivo |
| 🌊 **Aquáticas** | Sereia |
| 🏔️ **Selvagens** | Centauro, Trol, Rinoceronte |
| 🌟 **Mágicas** | Djinn, Fauno, Gnomo |
| 🍀 **Folclóricas** | Leprechaun, Goblin |

### 🎨 **Sistema Visual**

- **📸 Retratos:** Cada líder possui arte única e detalhada
- **🏰 Reinos:** Ambientações visuais matching com as espécies
- **🎭 Consistência:** Arte coesa e profissional
- **📱 Interface:** Layout responsivo e intuitivo

---

## 🖼️ Interface Gráfica

### 🖥️ **Tela Principal**

```
┌─────────────────────────────────────┐
│  🎮 RPG GRÁFICO COM GEMINI          │
├─────────────────────────────────────┤
│                                     │
│    🖼️ [Imagem do Líder]            │
│                                     │
│    👑 Nome: [Input]                 │
│    🏰 Reino: [Input]                │
│                                     │
│    [🎭 Seleção de Espécie]          │
│                                     │
│    [▶️ Iniciar Jogo]                │
│                                     │
└─────────────────────────────────────┘
```

### 🎨 **Elementos Visuais**

| Componente | Descrição |
|------------|-----------|
| 🎭 **Galeria** | Grid visual com todas as espécies |
| 🖼️ **Preview** | Imagem grande da espécie selecionada |
| 📝 **Inputs** | Campos personalizados para nomes |
| 🎨 **Fonte** | Cinzel - fonte medieval elegante |
| 🎵 **Audio** | Sistema de música ambiente |

### 🖱️ **Navegação Intuitiva**

- ✅ **Clique** para selecionar espécies
- ✅ **Destaque visual** da seleção atual
- ✅ **Feedback** imediato nas interações
- ✅ **Layout responsivo** a diferentes resoluções

---

## 🎵 Sistema de Áudio

### 🎼 **Trilhas Sonoras Incluídas**

O jogo possui 6 ambientações musicais distintas:

| 🎵 Música | 🎭 Ambiente | 🎯 Uso |
|-----------|------------|--------|
| **🏃 Clima Frenético** | Ação/Combate | Batalhas e tensão |
| **🌅 Clima de Aventura** | Exploração | Descobertas e viagens |
| **😰 Clima de Desespero** | Drama/Crise | Momentos críticos |
| **🏗️ Clima de Desenvolvimento** | Construção | Crescimento do reino |
| **☮️ Clima Calmo** | Paz/Reflexão | Momentos tranquilos |
| **🎶 Clima de Harmonia** | Celebração | Vitórias e festivais |

### 🔊 **Características de Áudio**

- 🔄 **Loop contínuo** durante o jogo
- 🎚️ **Volume otimizado** para não interferir
- 🎵 **Qualidade MP3** para melhor experiência
- 🎧 **Som ambiente** imersivo

### ⚙️ **Configuração de Áudio**

```python
# O sistema de áudio é inicializado automaticamente
pygame.mixer.init()

# Música padrão: "clima de aventura.mp3"
# Localização: musicas/clima de aventura.mp3
```

---

## 🛠️ Recursos Visuais

### 🎨 **Fonte Personalizada: Cinzel**

**✨ Características:**
- 📚 **Estilo:** Medieval/Fantasy elegante
- 📏 **Variantes:** Regular, Bold, ExtraBold, Black
- 🎯 **Licença:** Open Font License (OFL)
- 🎮 **Uso:** Interface e textos do jogo

## 🐛 Solução de Problemas

### ❌ **"pygame.error: No available video device"**

**🔧 Solução para sistemas headless:**
```bash
# Definir display virtual
export DISPLAY=:0

# OU executar com Xvfb
xvfb-run -a python3 rpg_grafico.py
```

### ❌ **"ModuleNotFoundError: No module named 'pygame'"**

**🔧 Instalar pygame-ce:**
```bash
# Ativar ambiente virtual
source ../../../venv/bin/activate

# Instalar pygame-ce (Community Edition)
pip install pygame-ce pygame_gui
```

### ❌ **"FileNotFoundError: [Errno 2] No such file or directory: 'lideres/'"**

**🔧 Verificar estrutura de arquivos:**
```bash
# Verificar se as pastas existem
ls -la lideres/
ls -la reinos/
ls -la musicas/
ls -la Cinzel/

# Contar arquivos
ls lideres/ | wc -l    # Deve mostrar 19
ls reinos/ | wc -l     # Deve mostrar 19
ls musicas/ | wc -l    # Deve mostrar 6
```

### 🎵 **Problemas de Áudio**

**🔧 Solução:**
```bash
# Testar sistema de áudio
python3 -c "
import pygame
pygame.mixer.init()
print('✅ Audio OK')
"

# Verificar arquivos de música
ls -la musicas/*.mp3
```

### 🔧 **Comandos de Diagnóstico**

```bash
# Testar dependências completas
python3 -c "
import pygame
import pygame_gui
import google.generativeai as genai
print('✅ Todas dependências OK')
"