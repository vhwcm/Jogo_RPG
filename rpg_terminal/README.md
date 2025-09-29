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

### 📊 **Status do Reino**

Cada decisão afeta os seguintes parâmetros:

| Status | Faixa | Descrição |
|--------|-------|-----------|
| 😊 **Felicidade** | 0-100% | Satisfação dos cidadãos |
| ⚔️ **Poder Militar** | 0-100,000 | Força do exército |
| 🛐 **Religião** | Variável | Fé do reino (criada pelo jogo) |
| 💰 **Dinheiro** | 0-100,000 | Recursos econômicos |
| 🏰 **Nome do Reino** | Customizável | Sua criação |

### 🎲 **Tipos de Decisões**

#### 💼 **Econômicas**
- 💰 Gerenciar impostos e tributos
- 🛡️ Investir em infraestrutura
- 🚢 Estabelecer rotas comerciais
- 🏭 Desenvolver indústrias

#### 🛐 **Religiosas**
- ⛪ Escolher divindades do reino
- 🎭 Estabelecer festivais e rituais
- 👨‍💼 Gerenciar clero e templos
- ⚖️ Definir leis baseadas na fé

#### ⚔️ **Militares**
- 🗡️ Treinar tropas e comandantes
- 🏰 Construir fortificações
- 🛡️ Formar alianças defensivas
- ⚔️ Declarar guerras ou negociar paz

#### 🤝 **Diplomáticas**
- 👑 Negociar com outros reinos
- 💍 Arranjar casamentos políticos
- 📜 Estabelecer tratados
- 🕊️ Resolver conflitos pacificamente

### 🎯 **Sistema de Consequências**

- 📈 **Decisões sábias** aumentam status positivos
- 📉 **Escolhas imprudentes** podem causar revoltas
- ⚖️ **Equilíbrio** é fundamental para o sucesso
- 🎲 **Eventos aleatórios** desafiam sua estratégia

---

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

## 🔧 Comandos e Controles

### 💬 **Interação com o Jogo**

```bash
# Exemplos de comandos válidos:

# ✅ Escolher opções numeradas
PROMPT: 1

# ✅ Fazer perguntas
PROMPT: Como está a economia do meu reino?

# ✅ Dar ordens específicas
PROMPT: Quero investir em agricultura

# ✅ Solicitar informações
PROMPT: Me conte sobre os reinos vizinhos

# ✅ Sair do jogo
PROMPT: fim
```

### 🎭 **Dicas de Interação**

| ✅ **Faça** | ❌ **Evite** |
|-------------|--------------|
| Seja específico nas perguntas | Comandos muito vagos |
| Use as opções numeradas | Respostas muito longas |
| Pergunte detalhes quando em dúvida | Decisões sem pensar |
| Mantenha consistência de personagem | Mudar personalidade drasticamente |

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

# Verificar pasta mundos
ls -la mundos/
```

---

## 💡 Dicas Avançadas

### 🎯 **Estratégias de Jogo**

#### 🏁 **Para Iniciantes**
- 📊 **Equilibre** os 4 status principais
- 🤝 **Forme** alianças antes de declarar guerras
- 💰 **Invista** em economia antes de exército
- 😊 **Mantenha** a felicidade do povo em alta

#### 🎖️ **Para Avançados**
- 🎲 **Experimente** estratégias arriscadas
- 🔍 **Explore** perguntas complexas ao Gemini
- 🎭 **Desenvolva** uma personalidade consistente
- 📈 **Otimize** decisões baseadas em padrões observados

### 📚 **Roleplay Avançado**

```bash
# Exemplos de perguntas imersivas:

PROMPT: Como está o moral das tropas após a última batalha?

PROMPT: Qual é a opinião do povo sobre minha liderança?

PROMPT: Existem rumores de conspirações na corte?

PROMPT: Como posso melhorar as relações diplomáticas?
```

### 🎨 **Personalização da Experiência**

- 🎭 **Crie** backstories detalhadas para seu reino
- 🏰 **Desenvolva** tradições e costumes únicos
- 👥 **Imagine** personagens importantes (conselheiros, generais)
- 🌍 **Construa** um mundo consistente ao longo do tempo

### 📊 **Análise de Performance**

Monitore seus status ao longo do tempo:

```
Início:   😊 70%  ⚔️ 3000   💰 5000
Após 10 turnos: 😊 85%  ⚔️ 4500   💰 7200
Meta:     😊 90%+ ⚔️ 8000+ 💰 15000+
```

---

## 🔗 **Links Relacionados**

- 🎨 **[RPG Gráfico](../rpg_grafico/README.md)** - Versão visual do jogo
- 📚 **[Configuração Completa](../../CONFIGURACAO_AMBIENTE.md)** - Guia detalhado
- 🤖 **[Modelos Gemini](../../MODELOS_GEMINI.md)** - Informações sobre IA
- 🔧 **[Mudanças Técnicas](../../MUDANCAS_TECNICAS.md)** - Log de atualizações

---

## ⭐ **Recursos Únicos**

### 🎯 **Diferenciadores**

| Recurso | Descrição |
|---------|-----------|
| 🤖 **IA Criativa** | Gemini 2.5 Pro gera conteúdo único |
| 🌟 **Espécies Ilimitadas** | Qualquer conceito que imaginar |
| 📚 **Contexto Persistente** | História mantida entre sessões |
| 🎭 **Roleplay Profundo** | Interação natural e imersiva |
| 💾 **Save Flexível** | Sistema de arquivo simples e confiável |

### 🏆 **Achievements Sugeridos**

- 👑 **Primeiro Reino** - Crie seu primeiro reino
- 🕊️ **Pacifista** - Resolva 5 conflitos sem guerra
- 💰 **Magnata** - Acumule 50,000 em dinheiro
- 😊 **Amado** - Mantenha felicidade acima de 90%
- ⚔️ **Conquistador** - Vença 3 guerras consecutivas

---

<div align="center">

**🎭 Governe com sabedoria, lidere com coragem! 👑**

---

*RPG Terminal é uma experiência única de estratégia alimentada por IA*

</div>