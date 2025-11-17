#!/usr/bin/env python3
"""
Suite de testes para a API de Scraping do Mercado Livre
Testa todos os endpoints e cenários de autenticação
"""

import requests
import json
from datetime import datetime

# Configuração
API_URL = "http://localhost:8000"
VALID_TOKEN = "seu_token_secreto_super_seguro_aqui"
INVALID_TOKEN = "token_invalido_123456"
TEST_URL = "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848"

# Cores para output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Tracking de testes
testes_passaram = 0
testes_falharam = 0
resultados = []

def print_teste(numero, nome, resultado, detalhes=""):
    """Exibe resultado de um teste"""
    global testes_passaram, testes_falharam
    
    if resultado:
        testes_passaram += 1
        status = f"{GREEN}✅ PASSOU{RESET}"
    else:
        testes_falharam += 1
        status = f"{RED}❌ FALHOU{RESET}"
    
    print(f"{status} - {nome}")
    if detalhes:
        print(f"   {BLUE}→ {detalhes}{RESET}")
    
    resultados.append({
        "numero": numero,
        "nome": nome,
        "passou": resultado,
        "detalhes": detalhes
    })

def teste_1_status():
    """Teste 1: Verificar endpoint /status"""
    try:
        response = requests.get(f"{API_URL}/status", timeout=5)
        passou = response.status_code == 200 and response.json().get("online")
        detalhes = f"Status: {response.status_code}, Online: {response.json().get('online')}"
        print_teste(1, "Status da API", passou, detalhes)
    except Exception as e:
        print_teste(1, "Status da API", False, f"Erro: {str(e)}")

def teste_2_root():
    """Teste 2: Verificar endpoint raiz /"""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        passou = response.status_code == 200
        detalhes = f"Status: {response.status_code}, Message: {response.json().get('message', 'N/A')[:50]}"
        print_teste(2, "Informações da API", passou, detalhes)
    except Exception as e:
        print_teste(2, "Informações da API", False, f"Erro: {str(e)}")

def teste_3_scrape_sem_token():
    """Teste 3: Scraping SEM token (deve falhar com 401)"""
    try:
        payload = {
            "url": TEST_URL,
            "capturar_screenshots": False
        }
        response = requests.post(f"{API_URL}/scrape", json=payload, timeout=5)
        passou = response.status_code == 401
        detalhes = f"Status: {response.status_code} (esperado 401)"
        print_teste(3, "Scraping SEM Token (deve falhar)", passou, detalhes)
    except Exception as e:
        print_teste(3, "Scraping SEM Token (deve falhar)", False, f"Erro: {str(e)}")

def teste_4_scrape_token_invalido():
    """Teste 4: Scraping com token INVÁLIDO (deve falhar com 401)"""
    try:
        headers = {
            "Authorization": f"Bearer {INVALID_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "url": TEST_URL,
            "capturar_screenshots": False
        }
        response = requests.post(f"{API_URL}/scrape", headers=headers, json=payload, timeout=5)
        passou = response.status_code == 401
        detalhes = f"Status: {response.status_code} (esperado 401)"
        print_teste(4, "Scraping com token INVÁLIDO (deve falhar)", passou, detalhes)
    except Exception as e:
        print_teste(4, "Scraping com token INVÁLIDO (deve falhar)", False, f"Erro: {str(e)}")

def teste_5_scrape_token_valido():
    """Teste 5: Scraping COM token VÁLIDO (deve funcionar)"""
    try:
        headers = {
            "Authorization": f"Bearer {VALID_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "url": TEST_URL,
            "capturar_screenshots": False
        }
        print(f"\n   {YELLOW}⏳ Aguardando resposta do scraping (pode levar 15-20s)...{RESET}")
        response = requests.post(f"{API_URL}/scrape", headers=headers, json=payload, timeout=60)
        
        passou = response.status_code == 200 and response.json().get("sucesso")
        
        if passou:
            dados = response.json().get("dados", {})
            titulo = dados.get("titulo", "N/A")[:40]
            detalhes = f"Status: {response.status_code}, Título: {titulo}..."
        else:
            detalhes = f"Status: {response.status_code}, Sucesso: {response.json().get('sucesso')}"
        
        print_teste(5, "Scraping COM Token VÁLIDO (deve funcionar)", passou, detalhes)
    except Exception as e:
        print_teste(5, "Scraping COM Token VÁLIDO (deve funcionar)", False, f"Erro: {str(e)}")

def teste_6_lista_screenshots():
    """Teste 6: Listar screenshots disponíveis"""
    try:
        headers = {
            "Authorization": f"Bearer {VALID_TOKEN}"
        }
        response = requests.get(f"{API_URL}/screenshots/list", headers=headers, timeout=5)
        passou = response.status_code == 200
        screenshots_count = len(response.json().get("screenshots", []))
        detalhes = f"Status: {response.status_code}, Screenshots: {screenshots_count}"
        print_teste(6, "Listar screenshots", passou, detalhes)
    except Exception as e:
        print_teste(6, "Listar screenshots", False, f"Erro: {str(e)}")

def main():
    """Executar todos os testes"""
    print(f"\n{BOLD}{BLUE}{'='*60}")
    print(f"🧪 SUITE DE TESTES - API MERCADO LIVRE SCRAPER")
    print(f"{'='*60}{RESET}\n")
    
    print(f"{BLUE}Conectando em: {API_URL}{RESET}\n")
    
    # Executar testes
    teste_1_status()
    print()
    teste_2_root()
    print()
    teste_3_scrape_sem_token()
    print()
    teste_4_scrape_token_invalido()
    print()
    teste_5_scrape_token_valido()
    print()
    teste_6_lista_screenshots()
    
    # Resumo
    print(f"\n{BOLD}{BLUE}{'='*60}")
    print(f"📊 RESUMO DOS TESTES")
    print(f"{'='*60}{RESET}\n")
    
    total = testes_passaram + testes_falharam
    percentual = (testes_passaram / total * 100) if total > 0 else 0
    
    print(f"Total de testes: {total}")
    print(f"{GREEN}✅ Passaram: {testes_passaram}{RESET}")
    print(f"{RED}❌ Falharam: {testes_falharam}{RESET}")
    print(f"Percentual de sucesso: {percentual:.1f}%\n")
    
    if testes_falharam == 0:
        print(f"{GREEN}{BOLD}🎉 TODOS OS TESTES PASSARAM! 🎉{RESET}\n")
    else:
        print(f"{RED}{BOLD}⚠️  ALGUNS TESTES FALHARAM{RESET}\n")
    
    print(f"{BLUE}{'='*60}{RESET}\n")

if __name__ == "__main__":
    main()
