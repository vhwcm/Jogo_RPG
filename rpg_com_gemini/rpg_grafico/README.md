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

Se ainda não configurou o ambiente, execute no diretório raiz:

```bash
# Configuração automática
./setup.sh

# OU configuração manual
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

### 🖼️ **Sistema de Imagens**

#### **📐 Especificações Técnicas:**
- **🔍 Formato:** JPEG/PNG
- **📊 Qualidade:** Alta resolução
- **🎨 Estilo:** Arte fantástica consistente
- **📱 Compatibilidade:** Otimizado para Pygame

#### **🗂️ Organização de Assets:**

```
lideres/
├── humano.jpeg      🧑 Humano clássico
├── elfo.jpeg        🧝 Elfo élfico
├── anão.jpeg        🔨 Anão robusto
├── dragão.jpeg      🐲 Dragão majestoso
├── mago.jpeg        🧙 Mago sábio
├── vampiro.jpeg     🧛 Vampiro sombrio
├── sereia.jpeg      🧜 Sereia aquática
├── centauro.jpg     🐎 Centauro selvagem
├── demonio.jpeg     😈 Demônio poderoso
├── djinn.jpeg       🧞 Djinn místico
├── elemental.jpeg   🌟 Elemental mágico
├── fauno.jpeg       🐐 Fauno da floresta
├── gnomo.jpeg       👨‍🌾 Gnomo trabalhador
├── goblin.jpeg      👹 Goblin astuto
├── Leprechaun.jpeg  🍀 Leprechaun sortudo
├── morto vivo.jpeg  💀 Morto-vivo sinistro
├── orc.jpeg         👹 Orc guerreiro
├── rinoceronte.jpeg 🦏 Rinoceronte forte
└── trol.jpeg        👹 Trol gigante
```

### 🏰 **Imagens dos Reinos**

Cada espécie possui um reino visual correspondente:

```
reinos/
├── reino humano.png      🏰 Castelo humano
├── reino elfo.png        🌳 Floresta élfica  
├── reino anão.png        ⛰️ Montanha anã
├── reino dragão.png      🌋 Covil do dragão
└── ... (19 reinos total)
```

---

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

### ⚠️ **Problemas de Performance**

**💡 Otimizações:**
```python
# Verificar FPS
pygame.time.Clock().tick(60)

# Monitorar memoria
import psutil
print(f"Uso de RAM: {psutil.virtual_memory().percent}%")
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

# Verificar recursos visuais
find . -name '*.jpeg' -o -name '*.jpg' -o -name '*.png' | wc -l

# Testar fonte
python3 -c "
import pygame
pygame.font.init()
font = pygame.font.Font('Cinzel/Cinzel-VariableFont_wght.ttf', 24)
print('✅ Fonte Cinzel carregada')
"
```

---

## 🎨 Personalização

### 🎨 **Modificar Interface**

#### **🎨 Cores e Temas:**
```python
# Localizar no código (rpg_grafico.py)
CORES = {
    'background': (50, 50, 50),      # Fundo escuro
    'text': (255, 255, 255),         # Texto branco
    'button': (100, 100, 100),       # Botões cinza
    'highlight': (200, 200, 200)     # Destaque claro
}
```

#### **📐 Dimensões da Janela:**
```python
# Modificar resolução (linha ~100)
largura_tela = 1200  # Largura
altura_tela = 800    # Altura
```

### 🎵 **Personalizar Áudio**

#### **➕ Adicionar Novas Músicas:**
1. 📁 Coloque arquivos `.mp3` na pasta `musicas/`
2. 🔧 Modifique o código para incluir novos tracks
3. 🎵 Use nomes descritivos para facilitar seleção

#### **🎚️ Controle de Volume:**
```python
# Ajustar volume (0.0 a 1.0)
pygame.mixer.music.set_volume(0.5)  # 50% do volume
```

### 🖼️ **Adicionar Novas Espécies**

#### **📋 Passos:**
1. **🎨 Arte:** Crie imagem do líder (`nova_especie.jpeg`)
2. **🏰 Reino:** Crie imagem do reino (`reino nova_especie.png`)
3. **📁 Organização:** Coloque nas pastas `lideres/` e `reinos/`
4. **💻 Código:** Adicione à lista no código:

```python
# Adicionar nova espécie na lista (linha ~150)
especies = [
    'humano', 'elfo', 'anão', 'orc',
    'dragão', 'mago', 'elemental',
    'nova_especie'  # 👈 Sua nova espécie
]
```

### 🎭 **Customizar Experiência**

#### **⚙️ Configurações Avançadas:**
```python
# Personalizar fonte e tamanhos
FONTE_TITULO = 32
FONTE_NORMAL = 24  
FONTE_PEQUENA = 18

# Ajustar grid de espécies
COLUNAS_ESPECIES = 6  # Espécies por linha
TAMANHO_PREVIEW = 200  # Tamanho da imagem preview
```

---

### 🖥️ **Compatibilidade de Sistemas**

#### **✅ Linux (Recomendado)**
- 🐧 **Ubuntu/Debian:** Funciona perfeitamente
- 🎩 **Fedora/RHEL:** Compatível
- 🏔️ **Arch/Manjaro:** Suporte completo

#### **🪟 Windows**
- ✅ **Windows 10/11:** Totalmente compatível
- 💡 **Recomendado:** Executar diretamente no Windows

#### **⚠️ WSL (Windows Subsystem for Linux)**
- 🚫 **Limitações:** Problemas com interface gráfica
- 💡 **Solução:** Use X11 forwarding ou rode no Windows nativo
- 🔧 **Alternativa:** Executar diretamente no Windows

#### **🍎 macOS**
- ✅ **macOS 10.15+:** Funciona com Pygame-CE
- 🛠️ **Configuração:** Pode precisar de ajustes no Homebrew

---

## 🔗 **Links Relacionados**

- 🖥️ **[RPG Terminal](../rpg_terminal/README.md)** - Versão texto do jogo
- 📚 **[Configuração Completa](../../CONFIGURACAO_AMBIENTE.md)** - Guia detalhado
- 🔧 **[Mudanças Técnicas](../../MUDANCAS_TECNICAS.md)** - Log de atualizações
- 🎨 **[Assets do Jogo](./lideres/)** - Recursos visuais

---

## ⭐ **Recursos Únicos**

### 🎯 **Diferenciadores**

| Recurso | Descrição |
|---------|-----------|
| 🎨 **Interface Rica** | Pygame-CE com elementos visuais |
| 🎭 **19 Espécies** | Galeria visual interativa |
| 🎵 **Sistema de Áudio** | 6 trilhas ambientais |
| ✒️ **Fonte Medieval** | Tipografia Cinzel personalizada |
| 🖼️ **Arte Consistente** | Líderes e reinos harmonizados |
| 🤖 **IA Gemini** | Narrativa dinâmica e criativa |

### 🎮 **Comparação com Versão Terminal**

| Aspecto | 🖥️ Terminal | 🎮 Gráfico |
|---------|-------------|------------|
| **Interface** | Texto puro | Visual rica |
| **Seleção** | Digitação | Clique visual |
| **Imersão** | Imaginação | Assets visuais |
| **Áudio** | Nenhum | Trilha sonora |
| **Recursos** | Mínimos | Completos |
| **Performance** | Leve | Moderada |

### 🏆 **Experiência Premium**

- 🎨 **Visual Storytelling** através de imagens
- 🎵 **Ambiente sonoro** imersivo
- 🖱️ **Navegação intuitiva** point-and-click
- 🎭 **Apresentação profissional** dos personagens
- 🌟 **Experiência cinematográfica** de RPG

---

<div align="center">

**🎮 Uma aventura visual épica te aguarda! 🏰**

---

*RPG Gráfico combina o poder do Gemini AI com uma interface rica e envolvente*

</div>

