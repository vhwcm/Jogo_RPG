#!/bin/bash

# 🎮 Mini Games - Script de Configuração Automática
# Este script configura automaticamente o ambiente para os jogos RPG

echo "🎮 Configurando ambiente para Mini Games..."
echo "========================================"

# Verificar se Python está instalado
echo "🐍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

python_version=$(python3 --version | cut -d" " -f2 | cut -d"." -f1,2)
echo "✅ Python $python_version encontrado"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se pip está atualizado
echo "📦 Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1

# Instalar dependências
echo "📚 Instalando dependências..."
echo "  - Google Generative AI..."
pip install google-generativeai > /dev/null 2>&1

echo "  - Pygame Community Edition..."
pip install pygame-ce > /dev/null 2>&1

echo "  - Pygame GUI..."
pip install pygame_gui > /dev/null 2>&1

# Verificar instalação
echo ""
echo "🔍 Verificando instalação..."

# Testar Google Generative AI
if python3 -c "import google.generativeai as genai; print('✅ Google Generative AI')" 2>/dev/null; then
    echo "✅ Google Generative AI instalado corretamente"
else
    echo "❌ Erro na instalação do Google Generative AI"
fi

# Testar Pygame-CE
if python3 -c "import pygame; print('✅ Pygame-CE')" 2>/dev/null; then
    echo "✅ Pygame-CE instalado corretamente"
else
    echo "❌ Erro na instalação do Pygame-CE"
fi

# Testar Pygame GUI
if python3 -c "import pygame_gui; print('✅ Pygame GUI')" 2>/dev/null; then
    echo "✅ Pygame GUI instalado corretamente"
else
    echo "❌ Erro na instalação do Pygame GUI"
fi

# Criar pastas necessárias
echo ""
echo "📁 Criando estrutura de pastas..."
mkdir -p rpg_com_gemini/rpg_terminal/mundos
mkdir -p rpg_com_gemini/rpg_grafico/mundos
echo "✅ Pastas criadas"

echo ""
echo "🎉 Configuração concluída!"
echo "========================================"
echo ""
echo "📋 Próximos passos:"
echo "1. 🔑 Configure sua chave API do Gemini nos arquivos:"
echo "   - rpg_com_gemini/rpg_terminal/rpg.py (linha 12)"
echo "   - rpg_com_gemini/rpg_grafico/rpg_grafico.py (linha 19-20)"
echo ""
echo "2. 🎮 Execute os jogos:"
echo "   ./executar_jogos.sh"
echo ""
echo "3. 🔍 Para verificar a configuração:"
echo "   ./verificar_config.sh"
echo ""
echo "📖 Consulte o README.md para instruções detalhadas."