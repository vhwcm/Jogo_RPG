#!/bin/bash

# 🎮 Mini Games - Script de Execução
# Este script permite executar facilmente os jogos RPG

echo "🎮 Mini Games - Launcher"
echo "========================"

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "🔧 Execute primeiro: ./setup.sh"
    exit 1
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Menu de seleção
echo ""
echo "🎯 Selecione o jogo que deseja executar:"
echo "1. 🖥️  RPG Terminal (texto)"
echo "2. 🎮 RPG Gráfico (visual)"
echo "3. 🔍 Verificar configuração"
echo "4. ❌ Sair"
echo ""

read -p "Digite sua opção (1-4): " opcao

case $opcao in
    1)
        echo ""
        echo "🖥️ Iniciando RPG Terminal..."
        echo "📍 Localização: rpg_com_gemini/rpg_terminal/"
        echo "⚠️  Certifique-se de ter configurado sua chave API!"
        echo ""
        cd rpg_com_gemini/rpg_terminal
        python3 rpg.py
        ;;
    2)
        echo ""
        echo "🎮 Iniciando RPG Gráfico..."
        echo "📍 Localização: rpg_com_gemini/rpg_grafico/"
        echo "⚠️  Certifique-se de ter configurado sua chave API!"
        echo ""
        
        # Verificar se há display disponível (importante para WSL/SSH)
        if [ -z "$DISPLAY" ]; then
            echo "⚠️  Variável DISPLAY não definida"
            echo "💡 Se estiver usando WSL, considere executar no Windows"
            echo "💡 Se estiver via SSH, configure X11 forwarding"
            echo ""
            read -p "Continuar mesmo assim? (s/N): " continuar
            if [[ ! $continuar =~ ^[Ss]$ ]]; then
                echo "❌ Execução cancelada"
                exit 1
            fi
        fi
        
        cd rpg_com_gemini/rpg_grafico
        python3 rpg_grafico.py
        ;;
    3)
        echo ""
        echo "🔍 Executando verificação de configuração..."
        ./verificar_config.sh
        ;;
    4)
        echo "👋 Até mais! Divirta-se jogando!"
        exit 0
        ;;
    *)
        echo "❌ Opção inválida! Digite um número entre 1 e 4."
        exit 1
        ;;
esac
