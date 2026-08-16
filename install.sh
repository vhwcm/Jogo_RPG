#!/bin/bash
# Unified installation script for AI RPG Game

echo "==========================================="
echo "  AI RPG Game - Instalação de Dependências "
echo "==========================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 não está instalado!"
    exit 1
fi

echo "Instalando dependências do projeto..."
pip3 install -r requirements.txt || python3 -m pip install -r requirements.txt --break-system-packages || python3 -m pip install --break-system-packages --user -r requirements.txt

echo ""
echo "==========================================="
echo " Instalação Concluída com Sucesso!"
echo "==========================================="
echo ""
echo "Comandos para iniciar:"
echo "  - Servidor Web (Interface Gráfica):  python3 run.py web"
echo "  - Executar Bateria de Testes:       python3 run.py test"
echo "  - Verificar Diagnóstico de APIs:    python3 run.py check"
echo ""
