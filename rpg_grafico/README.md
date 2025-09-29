# 🎮 RPG Gráfico - Aventura Visual com IA

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/Pygame--CE-2.5.5-red.svg)](https://pyga.me)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Pro-green.svg)](https://ai.google.dev)
[![GUI](https://img.shields.io/badge/Interface-Visual-purple.svg)](#)

> **RPG de aventura com interface gráfica e efeitos sonoros, powered by Google Gemini AI**

---

## 📋 Índice

- [🚀 Execução Rápida](#-execução-rápida)
- [⚙️ Configuração](#️-configuração)
- [🎮 Como Jogar](#-como-jogar)
- [🎭 Espécies Disponíveis](#-espécies-disponíveis)
- [🖼️ Interface Gráfica](#️-interface-gráfica)
- [🎵 Sistema de Áudio](#-sistema-de-áudio)
- [🛠️ Scripts Utilitários](#️-scripts-utilitários)
- [🐛 Solução de Problemas](#-solução-de-problemas)
- [🎨 Personalização](#-personalização)

---

## 🚀 Execução Rápida

### 📋 **Opção 1: Configuração Automática (Recomendada)**
```bash
# A partir do diretório raiz do projeto
./setup.sh                    # Configura ambiente automaticamente
./executar_jogos.sh           # Menu para iniciar jogos
```

### 📋 **Opção 2: Execução Manual**
```bash
# A partir do diretório raiz do projeto
source venv/bin/activate
cd rpg_com_gemini/rpg_grafico
python3 rpg_grafico.py
```

### 📋 **Pré-requisitos**
- ✅ Python 3.8+
- ✅ Chave API do Google Gemini
- ✅ Dependências instaladas (pygame-ce, pygame_gui)

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

### 📦 **2. Instalação das Dependências**

#### **🚀 Automática (Recomendada):**
```bash
# Execute no diretório raiz
./setup.sh
```

#### **🔧 Manual:**
```bash
# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install pygame-ce pygame_gui google-generativeai
```

### 🎨 **3. Recursos Visuais e Sonoros**

O jogo inclui assets organizados:

```
rpg_grafico/
├── 🖼️ lideres/          # Imagens dos líderes (19 espécies)
├── 🏰 reinos/           # Imagens dos reinos correspondentes
├── 🎵 musicas/          # Trilhas sonoras ambientais (6 faixas)
├── ✒️ Cinzel/           # Fonte personalizada medieval
└── 📄 rpg_grafico.py    # Código principal
```

---

## 🎮 Como Jogar

### 🏁 **Iniciando uma Nova Aventura**

1. ▶️ **Execute:** `python3 rpg_grafico.py`
2. 🖱️ **Clique** nas espécies para navegar
3. 🎭 **Escolha** sua espécie favorita
4. 📝 **Digite** seu nome de usuário
5. 🏰 **Digite** o nome do seu reino
6. 🌟 **Comece** sua aventura épica!

### 🖱️ **Controles**

| Controle | Função |
|----------|--------|
| 🖱️ **Mouse** | Navegação principal |
| 🖱️ **Clique** | Seleção de espécies e botões |
| ⌨️ **Teclado** | Digitação de nomes |
| 📝 **Enter** | Confirmar entradas |
| ❌ **Fechar janela** | Sair do jogo |

### 🎯 **Diferenças da Versão Terminal**

| Aspecto | 🖥️ Terminal | 🎮 Gráfico |
|---------|-------------|------------|
| **Interface** | Texto puro | Visual rica |
| **Seleção** | Digitação manual | Clique visual |
| **Espécies** | Ilimitadas | 19 pré-definidas |
| **Áudio** | Nenhum | Trilha sonora |
| **Status** | Misturado com texto | Interface separada |
| **Imersão** | Imaginação | Assets visuais |

---

## 🎭 Espécies Disponíveis

### 👑 **19 Espécies Únicas**

Cada espécie possui arte exclusiva do líder e reino correspondente:

#### 🌟 **Categorias:**

| 🏛️ **Clássicas** | 🐲 **Místicas** | 😈 **Sombrias** |
|------------------|-----------------|-----------------|
| Humano | Dragão | Demônio |
| Elfo | Mago | Vampiro |
| Anão | Elemental | Morto Vivo |
| Orc | Djinn | - |

| 🌊 **Aquáticas** | 🏔️ **Selvagens** | 🍀 **Folclóricas** |
|------------------|------------------|-------------------|
| Sereia | Centauro | Leprechaun |
| - | Trol | Goblin |
| - | Rinoceronte | Fauno |
| - | - | Gnomo |

### 🎨 **Sistema Visual**

- **📸 Retratos:** Arte única para cada líder
- **🏰 Reinos:** Ambientações visuais matching
- **🎭 Consistência:** Estilo artístico harmonioso
- **📱 Interface:** Layout responsivo e intuitivo

---

## 🖼️ Interface Gráfica

### 🖥️ **Layout Principal**

```
┌─────────────────────────────────────┐
│  🎮 RPG GRÁFICO COM GEMINI          │
├─────────────────────────────────────┤
│                                     │
│    🖼️ [Preview da Espécie]         │
│                                     │
│    👑 Nome: [_____________]         │
│    🏰 Reino: [____________]         │
│                                     │
│    [🎭 Grid de Espécies]            │
│                                     │
│    [▶️ Iniciar Aventura]            │
│                                     │
└─────────────────────────────────────┘
```

### 🎨 **Elementos Visuais**

| Componente | Descrição |
|------------|-----------|
| 🎭 **Galeria** | Grid interativo com 19 espécies |
| 🖼️ **Preview** | Imagem ampliada da espécie selecionada |
| 📝 **Campos** | Inputs personalizados para nomes |
| ✒️ **Fonte** | Cinzel - tipografia medieval elegante |
| 🎨 **Tema** | Interface dark com destaques visuais |

### 🖱️ **Experiência do Usuário**

- ✅ **Clique intuitivo** para navegar
- ✅ **Feedback visual** imediato
- ✅ **Destaque** da seleção atual
- ✅ **Responsividade** a diferentes resoluções

---

## 🎵 Sistema de Áudio

### 🎼 **6 Trilhas Ambientais**

| 🎵 Faixa | 🎭 Ambiente | 🎯 Contexto de Uso |
|-----------|------------|-------------------|
| **🏃 Clima Frenético** | Ação/Combate | Batalhas épicas e tensão |
| **🌅 Clima de Aventura** | Exploração | Descobertas e jornadas |
| **😰 Clima de Desespero** | Drama/Crise | Momentos críticos |
| **🏗️ Clima de Desenvolvimento** | Construção | Crescimento do reino |
| **☮️ Clima Calmo** | Paz/Reflexão | Momentos contemplativos |
| **🎶 Clima de Harmonia** | Celebração | Vitórias e festivais |

### 🔊 **Características**

- 🔄 **Loop contínuo** durante o gameplay
- 🎚️ **Volume balanceado** para não interferir
- 🎵 **Qualidade MP3** para experiência premium
- 🎧 **Áudio imersivo** que complementa a narrativa

---

## 🛠️ Scripts Utilitários

### 📋 **Scripts Disponíveis**

| Script | Função | Uso |
|--------|--------|-----|
| 🔧 **setup.sh** | Configuração automática | `./setup.sh` |
| ✅ **verificar_config.sh** | Diagnóstico do ambiente | `./verificar_config.sh` |
| 🎮 **executar_jogos.sh** | Menu de jogos | `./executar_jogos.sh` |

### 🚀 **Fluxo Recomendado**

```bash
# 1. Configurar ambiente
./setup.sh

# 2. Verificar instalação
./verificar_config.sh

# 3. Executar jogos
./executar_jogos.sh
```

---

## 🐛 Solução de Problemas

### ❌ **"pygame.error: No available video device"**

**🔧 Soluções:**
```bash
# Para WSL/Linux headless
export DISPLAY=:0

# Ou usar Xvfb
xvfb-run -a python3 rpg_grafico.py

# No Windows: executar diretamente (recomendado)
```

### ❌ **"ModuleNotFoundError: No module named 'pygame'"**

**🔧 Instalar pygame-ce:**
```bash
source venv/bin/activate
pip install pygame-ce pygame_gui
```

### ❌ **"FileNotFoundError: lideres/"**

**🔧 Verificar estrutura:**
```bash
# Verificar arquivos necessários
ls -la lideres/ | wc -l    # Deve mostrar 19
ls -la reinos/ | wc -l     # Deve mostrar 19
ls -la musicas/ | wc -l    # Deve mostrar 6
ls -la Cinzel/            # Deve mostrar fontes
```

### ⚠️ **Problemas de Performance**

**💡 Otimizações:**
- 🖥️ **Feche** outros programas pesados
- 🎮 **Use** resolução menor se necessário
- 💾 **Libere** espaço em disco
- 🔄 **Reinicie** o sistema se persistir

### 🎵 **Sem Áudio**

**🔧 Diagnóstico:**
```bash
# Testar pygame audio
python3 -c "
import pygame
pygame.mixer.init()
print('✅ Sistema de áudio OK')
"

# Verificar arquivos de música
ls -la musicas/*.mp3
```

### 🔧 **Script de Diagnóstico Completo**

```bash
# Execute para verificar tudo
./verificar_config.sh
```

---

## 🎨 Personalização

### 🎨 **Modificar Cores da Interface**

Edite `rpg_grafico.py` para personalizar:

```python
# Exemplo de personalização de cores
CORES = {
    'background': (30, 30, 30),      # Fundo mais escuro
    'text': (255, 255, 255),         # Texto branco
    'button': (70, 130, 180),        # Botões azul aço
    'highlight': (255, 215, 0)       # Destaque dourado
}
```

### 📐 **Ajustar Resolução**

```python
# Modificar dimensões da janela
largura_tela = 1400  # Largura personalizada
altura_tela = 900    # Altura personalizada
```

### 🎵 **Adicionar Novas Músicas**

1. 📁 Adicione arquivos `.mp3` na pasta `musicas/`
2. 🔧 Modifique o código para incluir novas faixas
3. 🎵 Use nomes descritivos para facilitar seleção

### 🖼️ **Criar Novas Espécies**

#### **📋 Processo:**
1. **🎨 Arte do Líder:** Crie `nova_especie.jpeg`
2. **🏰 Reino:** Crie `reino nova_especie.png`
3. **📁 Organização:** Coloque nas pastas corretas
4. **💻 Código:** Adicione à lista de espécies

```python
# Adicionar nova espécie (linha ~150)
especies = [
    'humano', 'elfo', 'anão', 'orc',
    'dragão', 'mago', 'elemental',
    'nova_especie'  # 👈 Sua criação
]
```

---

### 🖥️ **Compatibilidade de Sistemas**

#### **✅ Sistemas Suportados**

| SO | Status | Observações |
|----|--------|-------------|
| 🐧 **Linux** | ✅ Recomendado | Funciona perfeitamente |
| 🪟 **Windows** | ✅ Compatível | Performance otimizada |
| 🍎 **macOS** | ✅ Funciona | Pode precisar de ajustes |
| 🐧 **WSL** | ⚠️ Limitado | Problemas com GUI |

#### **💡 Recomendações por Sistema**

**🐧 Linux:**
- ✅ Experiência completa
- 🎮 Todos os recursos funcionais
- 🔊 Áudio e vídeo perfeitos

**🪟 Windows:**
- ✅ Melhor performance
- 🎯 Recomendado para iniciantes
- 📦 Instalação mais simples

**⚠️ WSL:**
- 🚫 Interface gráfica limitada
- 💡 Use X11 forwarding ou Windows nativo
- 🔧 Configuração complexa

---

## 🔗 **Links Relacionados**

- 🖥️ **[RPG Terminal](../rpg_terminal/README.md)** - Versão baseada em texto
- 📚 **[README Principal](../../README.md)** - Documentação completa
- 🎨 **[Assets Visuais](./lideres/)** - Galeria de recursos
- 🔧 **[Scripts Utilitários](../../)** - Automação e diagnóstico

---

## ⭐ **Recursos Únicos**

### 🎯 **Principais Diferenciadores**

| Recurso | Descrição |
|---------|-----------|
| 🎨 **Interface Rica** | Pygame-CE com elementos visuais profissionais |
| 🎭 **19 Espécies** | Galeria visual interativa com arte exclusiva |
| 🎵 **Sistema de Áudio** | 6 trilhas ambientais para imersão total |
| ✒️ **Fonte Medieval** | Tipografia Cinzel para atmosfera autêntica |
| 🖼️ **Arte Consistente** | Líderes e reinos harmonizados visualmente |
| 🤖 **IA Gemini 2.5** | Narrativa dinâmica e criativa |
| 📱 **UI Responsiva** | Interface que se adapta a diferentes telas |

### 🏆 **Experiência Premium**

- 🎨 **Visual Storytelling** através de imagens detalhadas
- 🎵 **Ambiente sonoro** que melhora a imersão
- 🖱️ **Navegação intuitiva** point-and-click
- 🎭 **Apresentação cinematográfica** dos personagens
- 🌟 **Jogo AAA independente** com produção cuidadosa

---

<div align="center">

**🎮 Uma aventura visual épica te aguarda! 🏰**

**🌟 Mergulhe em um mundo onde arte, música e IA se encontram! 🌟**

---

*RPG Gráfico: Onde a imaginação ganha vida através da tecnologia*

</div>

