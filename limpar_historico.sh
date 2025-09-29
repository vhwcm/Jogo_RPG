#!/bin/bash

# 🧹 Script para Limpar Histórico do Git
# Este script remove todos os commits anteriores, mantendo apenas o estado atual

echo "🧹 Limpando histórico do Git..."
echo "========================================"

# Verificar se estamos em um repositório git
if [ ! -d ".git" ]; then
    echo "❌ Erro: Este não é um repositório Git"
    exit 1
fi

# Fazer backup do branch atual
current_branch=$(git branch --show-current)
echo "📋 Branch atual: $current_branch"

# Verificar se há mudanças não commitadas
if ! git diff-index --quiet HEAD --; then
    echo "⚠️ Há mudanças não commitadas. Fazendo commit primeiro..."
    git add .
    git commit -m "🧹 Backup antes da limpeza do histórico"
fi

echo ""
echo "🔄 Iniciando processo de limpeza..."

# Criar um commit inicial órfão com todo o conteúdo atual
echo "📝 Criando novo commit inicial..."
git checkout --orphan temp_clean_branch

# Adicionar todos os arquivos
git add .

# Fazer o commit inicial
git commit -m "🎉 Estado inicial limpo - $(date '+%Y-%m-%d %H:%M:%S')"

# Renomear o branch temporário para main
echo "🔄 Atualizando branch principal..."
git branch -D main 2>/dev/null || true
git branch -m main

# Forçar push para o repositório remoto
echo "📤 Enviando para repositório remoto..."
git push --force-with-lease origin main

# Limpar branches temporários e remotos órfãos
echo "🧹 Limpando branches temporários..."
git remote prune origin
git gc --aggressive --prune=now

echo ""
echo "✅ Histórico limpo com sucesso!"
echo "========================================"
echo ""
echo "📊 Resumo:"
echo "• Todos os commits anteriores foram removidos"
echo "• Mantido apenas o estado atual do código"
echo "• Repositório remoto sincronizado"
echo "• Histórico limpo e otimizado"
echo ""
echo "📝 Para verificar:"
echo "git log --oneline"
echo ""
