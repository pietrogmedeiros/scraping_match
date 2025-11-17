#!/usr/bin/env python3
"""
Script de Deploy Automatizado para Vercel
Faz todo o processo de deployment da API
"""

import subprocess
import sys
import json
import os

def run_command(command, description=""):
    """Executa um comando e retorna o resultado"""
    print(f"\n{'='*60}")
    print(f"📍 {description}")
    print(f"{'='*60}")
    print(f"Executando: {command}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print("❌ Comando expirou (timeout)")
        return False, "", "Timeout"
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False, "", str(e)

def main():
    """Processo principal de deploy"""
    
    print("\n")
    print("🚀" * 30)
    print("\n   MERCADO LIVRE SCRAPER - DEPLOY VERCEL\n")
    print("🚀" * 30)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("api.py"):
        print("\n❌ Erro: Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # 1. Verificar Vercel CLI
    success, _, _ = run_command("vercel --version", "1️⃣ Verificar Vercel CLI")
    if not success:
        print("❌ Vercel CLI não encontrado!")
        sys.exit(1)
    
    # 2. Listar projetos existentes
    success, output, _ = run_command("vercel projects list", "2️⃣ Listar projetos Vercel")
    
    # 3. Fazer deploy para staging primeiro
    success, output, _ = run_command(
        "vercel --token ${VERCEL_TOKEN:-} 2>&1 | head -100",
        "3️⃣ Deploy para Staging"
    )
    
    if success:
        print("\n✅ Deploy para staging realizado!")
    else:
        print("\n⚠️  Continuando mesmo assim...")
    
    # 4. Informar próximos passos
    print(f"\n{'='*60}")
    print("📋 PRÓXIMAS ETAPAS")
    print(f"{'='*60}\n")
    
    print("1. Acesse o dashboard do Vercel:")
    print("   👉 https://vercel.com/dashboard\n")
    
    print("2. Selecione o projeto 'scraping-match'\n")
    
    print("3. Vá para Settings > Environment Variables\n")
    
    print("4. Adicione as variáveis:")
    print("   - API_TOKEN=seu_token_secreto_super_seguro_aqui")
    print("   - PORT=8000\n")
    
    print("5. Faça redeploy ou push para main branch\n")
    
    print("6. Teste a API:")
    print("   👉 https://seu-projeto.vercel.app/status\n")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
