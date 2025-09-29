#!/bin/bash

# 🔍 Mini Games - Verificador de Configuração
# Este script verifica se tudo está configurado corretamente

echo "🔍 Verificando Configuração do Mini Games"
echo "=========================================="

# Contador de problemas
problemas=0

# Verificar Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "✅ $python_version"
else
    echo "❌ Python3 não encontrado"
    ((problemas++))
fi

# Verificar ambiente virtual
echo ""
echo "📦 Verificando ambiente virtual..."
if [ -d "venv" ]; then
    echo "✅ Ambiente virtual existe"
    source venv/bin/activate
elif [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Ambiente virtual ativo: $VIRTUAL_ENV"
    
else
    echo "❌ Ambiente virtual não encontrado e não está ativo"
    ((problemas++))
fi

# Verificar dependências (se ambiente virtual estiver disponível)
if [ -d "venv" ] || [ -n "$VIRTUAL_ENV" ]; then
    echo ""
    echo "📚 Verificando dependências..."
    
    # Google Generative AI
    if python3 -c "import google.generativeai as genai" 2>/dev/null; then
        version=$(python3 -c "import google.generativeai as genai; print(genai.__version__)" 2>/dev/null)
        echo "✅ Google Generative AI v$version"
    else
        echo "❌ Google Generative AI não instalado"
        ((problemas++))
    fi
    
    # Pygame-CE
    if python3 -c "import pygame" 2>/dev/null; then
        version=$(python3 -c "import pygame; print(pygame.version.ver)" 2>/dev/null)
        echo "✅ Pygame-CE v$version"
    else
        echo "❌ Pygame-CE não instalado"
        ((problemas++))
    fi
    
    # Pygame GUI
    if python3 -c "import pygame_gui" 2>/dev/null; then
        version=$(python3 -c "import pygame_gui; print(pygame_gui.__version__)" 2>/dev/null)
        echo "✅ Pygame GUI v$version"
    else
        echo "❌ Pygame GUI não instalado"
        ((problemas++))
    fi
    
else
    echo "⚠️  Ambiente virtual não encontrado - pulando verificação de dependências"
    ((problemas++))
fi

# Verificar estrutura de arquivos
echo ""
echo "📁 Verificando estrutura de arquivos..."

# Arquivos principais
arquivos_principais=(
    "rpg_com_gemini/rpg_terminal/rpg.py"
    "rpg_com_gemini/rpg_grafico/rpg_grafico.py"
)

for arquivo in "${arquivos_principais[@]}"; do
    if [ -f "$arquivo" ]; then
        echo "✅ $arquivo"
    else
        echo "❌ $arquivo não encontrado"
        ((problemas++))
    fi
done

# Verificar pastas de recursos do RPG gráfico
echo ""
echo "🎨 Verificando recursos do RPG Gráfico..."

pastas_recursos=(
    "rpg_com_gemini/rpg_grafico/lideres"
    "rpg_com_gemini/rpg_grafico/reinos"
    "rpg_com_gemini/rpg_grafico/musicas"
    "rpg_com_gemini/rpg_grafico/Cinzel"
)

for pasta in "${pastas_recursos[@]}"; do
    if [ -d "$pasta" ]; then
        count=$(ls -1 "$pasta" 2>/dev/null | wc -l)
        echo "✅ $pasta ($count arquivos)"
    else
        echo "❌ $pasta não encontrada"
        ((problemas++))
    fi
done

# Verificar configuração da API
echo ""
echo "🔑 Verificando configuração da API..."

# Verificar RPG Terminal
if [ -f "rpg_com_gemini/rpg_terminal/rpg.py" ]; then
    if grep -q "SUA_CHAVE_AQUI\|SUA CHAVE DE API AQUI" rpg_com_gemini/rpg_terminal/rpg.py; then
        echo "⚠️  RPG Terminal: Chave API não configurada"
        ((problemas++))
    else
        echo "✅ RPG Terminal: Chave API configurada"
    fi
fi

# Verificar RPG Gráfico
if [ -f "rpg_com_gemini/rpg_grafico/rpg_grafico.py" ]; then
    if grep -q "SUA_CHAVE_DE_API_AQUI" rpg_com_gemini/rpg_grafico/rpg_grafico.py; then
        echo "⚠️  RPG Gráfico: Chave API não configurada"
        ((problemas++))
    else
        echo "✅ RPG Gráfico: Chave API configurada"
    fi
fi

# Verificar sistema gráfico (para RPG Gráfico)
echo ""
echo "🖥️ Verificando sistema gráfico..."
if [ -n "$DISPLAY" ]; then
    echo "✅ Variável DISPLAY definida: $DISPLAY"
elif [ -n "$WSL_DISTRO_NAME" ]; then
    echo "⚠️  Executando no WSL - pode ter problemas gráficos"
    echo "💡 Considere executar o RPG Gráfico no Windows diretamente"
else
    echo "⚠️  Variável DISPLAY não definida"
    echo "💡 Pode ter problemas para executar o RPG Gráfico"
fi

# Verificar conectividade com a API do Gemini
echo ""
echo "🌐 Verificando conectividade..."
if ping -c 1 google.com &> /dev/null; then
    echo "✅ Conexão com internet OK"
else
    echo "❌ Sem conexão com internet"
    ((problemas++))
fi

# Resumo final
echo ""
echo "📊 RESUMO DA VERIFICAÇÃO"
echo "========================"

if [ $problemas -eq 0 ]; then
    echo "🎉 Configuração perfeita! Tudo pronto para jogar!"
    echo ""
    echo "🎮 Execute os jogos com: ./executar_jogos.sh"
else
    echo "⚠️  Encontrados $problemas problema(s) na configuração"
    echo ""
    echo "🔧 Soluções sugeridas:"
    
    if [ ! -d "venv" ] || ! command -v python3 &> /dev/null; then
        echo "  • Execute: ./setup.sh"
    fi
    
    if grep -q "SUA_CHAVE\|SUA CHAVE DE API" rpg_com_gemini/*/rpg*.py 2>/dev/null; then
        echo "  • Configure sua chave API do Gemini"
        echo "    Obtenha em: https://aistudio.google.com"
    fi
    
    echo "  • Consulte o README.md para instruções detalhadas"
fi

echo ""
echo "📖 Para mais informações: README.md"
