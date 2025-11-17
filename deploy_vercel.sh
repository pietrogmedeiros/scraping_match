#!/bin/bash

# Script para fazer deploy na Vercel
# Este script automatiza todo o processo de deployment

set -e

echo "=========================================="
echo "🚀 Deploy Mercado Livre Scraper no Vercel"
echo "=========================================="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "api.py" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto"
    exit 1
fi

# 1. Verificar se Vercel CLI está instalado
echo "1️⃣ Verificando Vercel CLI..."
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI não encontrado. Instalando..."
    npm install -g vercel
fi

echo "✅ Vercel CLI OK"
echo ""

# 2. Verificar autenticação
echo "2️⃣ Verificando autenticação Vercel..."
if ! vercel projects list &> /dev/null; then
    echo "⚠️  Você precisa fazer login no Vercel"
    echo "Executando: vercel login"
    vercel login
fi
echo "✅ Autenticação OK"
echo ""

# 3. Fazer deploy
echo "3️⃣ Iniciando deploy..."
echo "Enviando para: https://vercel.com/"
echo ""

# Deploy com production flag
vercel --prod

echo ""
echo "=========================================="
echo "✅ Deploy realizado com sucesso!"
echo "=========================================="
echo ""
echo "📍 Próximos passos:"
echo "1. Acesse seu projeto em: https://vercel.com/dashboard"
echo "2. Configure as variáveis de ambiente:"
echo "   - API_TOKEN=seu_token_secreto"
echo "   - PORT=8000"
echo "3. Aguarde a construção finalizar"
echo "4. Teste: https://seu-projeto.vercel.app/status"
echo ""
