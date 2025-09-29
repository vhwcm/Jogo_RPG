# 🖥️ RPG Terminal - Estratégia com IA

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Pro-green.svg)](https://ai.google.dev)
[![Terminal](https://img.shields.io/badge/Interface-Terminal-black.svg)](#)

> **RPG de estratégia baseado em texto, desenvolvido com Google Gemini AI**

---

## 📋 Índice

- [🚀 Execução Rápida](#-execução-rápida)
- [⚙️ Configuração](#️-configuração)
- [🎮 Como Jogar](#-como-jogar)
- [🎯 Mecânicas do Jogo](#-mecânicas-do-jogo)
- [📁 Sistema de Salvamento](#-sistema-de-salvamento)
- [🔧 Comandos e Controles](#-comandos-e-controles)
- [🐛 Solução de Problemas](#-solução-de-problemas)
- [💡 Dicas Avançadas](#-dicas-avançadas)

---

## 🚀 Execução Rápida

```bash
# A partir do diretório raiz do projeto
source venv/bin/activate
cd rpg_com_gemini/rpg_terminal
python3 rpg.py
```

### 📋 **Pré-requisitos**
- ✅ Ambiente virtual ativado
- ✅ Dependências instaladas
- ✅ Chave API configurada

---

## ⚙️ Configuração

### 🔑 **1. Chave API do Google Gemini**

#### **Obter Chave:**
1. 🌐 Acesse: **[Google AI Studio](https://aistudio.google.com)**
2. 🔐 Faça login e crie uma chave API **gratuita**
3. 📋 Copie a chave gerada

#### **Configurar no Código:**
📝 **Edite o arquivo `rpg.py`, linha 12:**

```python
API_KEY = 'SUA_CHAVE_AQUI'  # 👈 Substitua pela sua chave real
```

### 📦 **2. Dependências**

Se ainda não configurou o ambiente, execute no diretório raiz:

```bash
# Configuração automática
./setup.sh

# OU configuração manual
source venv/bin/activate
pip install google-generativeai
```

### 📁 **3. Pasta de Salvamentos**

A pasta `mundos/` é criada **automaticamente** para armazenar seus jogos salvos.

---

## 🎮 Como Jogar

### 🏁 **Iniciando o Jogo**

1. ▶️ **Execute:** `python3 rpg.py`
2. 📝 **Escolha** um nome para sua aventura
3. 👑 **Defina** seu nome, reino e raça
4. 🆕 **Escolha** se é um novo reino ou continuação

### 🌟 **Espécies Disponíveis**

> **🎭 Qualquer espécie que você imaginar!**

O Gemini AI é extremamente criativo e aceita qualquer conceito:

- 🏛️ **Clássicas:** Elfos, Anões, Humanos, Orcs
- 🐲 **Fantásticas:** Dragões, Fênix, Unicórnios
- 🚀 **Futuristas:** Cyborgs, Aliens, Androides  
- 🌊 **Aquáticas:** Sereias, Polvos, Golfinhos
- 🔮 **Místicas:** Elementais, Espíritos, Demônios
- 🦄 **Únicas:** Suas próprias criações!

### 📜 **Comandos Especiais**

| Comando | Função |
|---------|--------|
| 📝 **Qualquer texto** | Interagir com o jogo |
| 🔢 **Números (1, 2, 3...)** | Escolher opções |
| ❓ **Perguntas** | Pedir detalhes ao Gemini |
| 🔚 **"fim"** | Sair do jogo |

### 💾 **Continuando Aventuras**

Para retomar uma aventura anterior:
1. 📛 Use o **mesmo nome de aventura**
2. 👑 Use o **mesmo nome de personagem**
3. 🏰 Use o **mesmo nome de reino**
4. 🎭 Use a **mesma raça**
5. ✅ Responda **"sim"** quando perguntado se já possui reino

---

## 🎯 Mecânicas do Jogo

## 📁 Sistema de Salvamento

### 💾 **Como Funciona**

```
mundos/
├── aventura1.txt          # Sua primeira aventura
├── reino_dragoes.txt      # Reino dos dragões
├── imperio_espacial.txt   # Império do espaço
└── ...                    # Mais aventuras
```

### 🔄 **Características**

- ✅ **Salvamento automático** após cada interação
- 📝 **Formato texto** legível e editável
- 🎮 **Multiplayer básico** - múltiplos jogadores no mesmo arquivo
- 📚 **Histórico completo** de todas as ações
- 🔁 **Continuidade** entre sessões

### ⚠️ **Multiplayer (Experimental)**

> **Possível via SSH, mas com limitações:**

- 👥 Dois jogadores podem jogar **simultaneamente**
- ⏱️ **Evite** enviar mensagens ao mesmo tempo
- 🚫 **Cota da API** pode ser esgotada rapidamente
- 💡 **Recomendado:** Jogar em turnos

---

## 🐛 Solução de Problemas

### ❌ **"No module named 'google.generativeai'"**

```bash
# Ativar ambiente virtual
source ../../venv/bin/activate

# Instalar dependência
pip install google-generativeai
```

### ❌ **"API key not configured"**

1. ✅ Verifique se substituiu `'SUA CHAVE DE API AQUI'` pela chave real
2. ✅ Confirme que a chave está entre aspas simples
3. ✅ Teste a chave em: [aistudio.google.com](https://aistudio.google.com)

### ⚠️ **"Rate limit exceeded"**

- ⏱️ **Aguarde** alguns minutos antes de tentar novamente
- 🚫 **Evite** múltiplas sessões simultâneas
- 💡 **Use** o modo multiplayer com moderação

### ❌ **Jogo não inicia**

1. 🌐 **Verifique** conexão com internet
2. 🔑 **Confirme** que a chave API está válida
3. 🐍 **Certifique-se** que está no ambiente virtual correto
4. 📁 **Verifique** se está no diretório correto

### 🔧 **Comandos de Diagnóstico**

```bash
# Testar dependências
python3 -c "import google.generativeai as genai; print('✅ Gemini OK')"

# Testar API
python3 -c "
import google.generativeai as genai
genai.configure(api_key='SUA_CHAVE')
print('✅ API funcionando')
"