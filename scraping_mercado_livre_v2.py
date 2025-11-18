"""
Scraper para Mercado Livre - Versão 2.1 (Otimizada com requests + BeautifulSoup)
Usa requests para carregar a página e BeautifulSoup para parsing
Muito mais rápido e confiável que Playwright para Vercel
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List


def scrape_mercado_livre(url: str, capturar_screenshots: bool = False) -> Dict:
    """
    Realiza scraping de um produto do Mercado Livre.
    
    Args:
        url: URL do produto no Mercado Livre
        capturar_screenshots: Se deve capturar screenshots (não implementado)
    
    Returns:
        Dict com dados extraídos: titulo, bullet_points, caracteristicas, cor, descricao
    """
    
    logs = []  # Coletar logs para retornar
    
    dados_produto = {
        "titulo": "N/A",
        "bullet_points": [],
        "caracteristicas": {},
        "cor": "N/A",
        "descricao": "N/A",
        "screenshots": {},
        "debug_logs": []
    }
    
    try:
        print(f"[INFO] Acessando URL: {url}")
        logs.append(f"Acessando URL: {url}")
        
        # Headers realistas para evitar bloqueio
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="131", "Chromium";v="131"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.mercadolivre.com.br/",
            "Connection": "keep-alive",
            "DNT": "1"
        }
        
        # Fazer requisição normal com requests
        response = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status()
        logs.append(f"Request bem-sucedido: {len(response.content)} bytes recebidos")
        
        print(f"[OK] Status: {response.status_code}")
        print(f"[DEBUG] Content length: {len(response.content)} bytes")
        print(f"[DEBUG] Content-Type: {response.headers.get('content-type')}")
        
        logs.append(f"Status: {response.status_code}")
        logs.append(f"Content-Length: {len(response.content)} bytes")
        logs.append(f"Content-Type: {response.headers.get('content-type')}")
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Verificar se tem conteúdo
        page_text = soup.get_text()
        print(f"[DEBUG] Page text length: {len(page_text)} caracteres")
        
        # Buscar títulos para debug
        h1s = soup.find_all('h1')
        print(f"[DEBUG] Total de h1s encontrados: {len(h1s)}")
        
        logs.append(f"Page text length: {len(page_text)} caracteres")
        logs.append(f"H1 elements found: {len(h1s)}")
        
        # DEBUG: Retornar snippet do HTML
        html_snippet = response.content[:500].decode('utf-8', errors='ignore')
        logs.append(f"HTML snippet: {html_snippet}")
        
        # Se página muito pequena, pode ser bloqueio
        if len(page_text) < 1000:
            logs.append("⚠️ AVISO: Página retornou com conteúdo muito pequeno - pode estar bloqueada!")
            logs.append(f"Content: {page_text[:200]}")
        
        # ============================================
        # 1. EXTRAIR TÍTULO (usando regex no texto bruto)
        # ============================================
        print("[DEBUG] Extraindo título...")
        # Procurar por padrões de título
        titulo_match = re.search(r'([A-Z][a-záàâãéèêíïóôõöúçñ0-9\s\-]{10,200}(?:Gallant|Britania|Mondial|Panificadora)[a-záàâãéèêíïóôõöúçñ0-9\s\-]{5,100}[0-9]w)', page_text)
        if titulo_match:
            dados_produto["titulo"] = titulo_match.group(1)[:200]
            print(f"[OK] Título encontrado: {dados_produto['titulo'][:50]}...")
            logs.append(f"Título: {dados_produto['titulo'][:50]}...")
        else:
            # Fallback: procurar primeira linha que parece ser um título
            h1 = soup.find('h1')
            if h1:
                dados_produto["titulo"] = h1.get_text(strip=True)[:200]
                logs.append(f"Título (via h1): {dados_produto['titulo'][:50]}...")
            else:
                # Tenta extrair do page_text
                lines = page_text.split('\n')
                for line in lines:
                    if len(line) > 15 and len(line) < 200 and 'Panificadora' in line or 'Britania' in line or 'Mondial' in line:
                        dados_produto["titulo"] = line.strip()
                        logs.append(f"Título (via regex): {dados_produto['titulo'][:50]}...")
                        break
        # ============================================
        # 2. EXTRAIR BULLET POINTS
        # ============================================
        print("[DEBUG] Extraindo bullet points...")
        bullet_points = []
        
        # Procurar por h2 "O que você precisa saber"
        h2_bullets = soup.find('h2', string=re.compile('você precisa saber', re.I))
        if h2_bullets:
            # Próximo elemento sibling contém os bullets
            container = h2_bullets.parent.find_next_sibling()
            if container:
                # Procurar ul com features-list
                ul = container.find('ul', {'class': re.compile('features-list', re.I)})
                if ul:
                    lis = ul.find_all('li')
                    print(f"[DEBUG] Encontrados {len(lis)} bullet points")
                    
                    for li in lis:
                        text = li.get_text(strip=True)
                        if text and len(text) > 10 and len(text) < 500:
                            if text not in bullet_points:
                                bullet_points.append(text)
        
        dados_produto["bullet_points"] = bullet_points
        if bullet_points:
            print(f"[OK] {len(bullet_points)} bullet points encontrados")
        
        # ============================================
        # 3. EXTRAIR CARACTERÍSTICAS
        # ============================================
        print("[DEBUG] Extraindo características...")
        caracteristicas = {}
        
        # Procurar por h2 "Características do produto"
        h2_char = soup.find('h2', string=re.compile('Características', re.I))
        if h2_char:
            # Próximo elemento sibling contém as characteristics
            container = h2_char.parent.find_next_sibling()
            if container:
                # Procurar divs com classe "key-value"
                key_value_divs = container.find_all('div', {'class': re.compile('key-value', re.I)})
                print(f"[DEBUG] Encontrados {len(key_value_divs)} pares chave-valor")
                
                for kv_div in key_value_divs:
                    # Dentro tem spans ou p com a chave e valor
                    spans = kv_div.find_all('span')
                    if len(spans) >= 2:
                        # Primeira span é a chave, segunda é o valor
                        chave = spans[0].get_text(strip=True)
                        valor = spans[1].get_text(strip=True)
                        
                        if chave and valor and len(chave) < 100 and len(valor) < 200:
                            # Remover ':'  da chave se existir
                            chave = chave.rstrip(':')
                            caracteristicas[chave] = valor
        
        dados_produto["caracteristicas"] = caracteristicas
        if caracteristicas:
            print(f"[OK] {len(caracteristicas)} características encontradas")
        
        # ============================================
        # 4. EXTRAIR COR (do texto bruto)
        # ============================================
        print("[DEBUG] Extraindo cor...")
        cor_match = re.search(r'Cor\s*:?\s*([A-Za-záàâãéèêíïóôõöúçñ]+(?:\s+[A-Za-záàâãéèêíïóôõöúçñ]+)?)\b', page_text, re.IGNORECASE)
        if cor_match:
            cor_text = cor_match.group(1).strip()
            if len(cor_text) < 50 and not any(w in cor_text.lower() for w in ['escolha', 'selecione', 'voltagem']):
                dados_produto["cor"] = cor_text
                print(f"[OK] Cor: {dados_produto['cor']}")
                logs.append(f"Cor: {dados_produto['cor']}")
        
        
        # ============================================
        # 5. EXTRAIR DESCRIÇÃO
        # ============================================
        print("[DEBUG] Extraindo descrição...")
        descricao = "N/A"
        
        # Procurar por h2 "Descrição"
        h2_desc = soup.find('h2', string=re.compile('Descrição', re.I))
        if h2_desc:
            container = h2_desc.parent
            
            # Próximo elemento após h2
            next_elem = container.find_next(['div', 'p', 'section'])
            if next_elem:
                desc_text = next_elem.get_text(strip=True)
                if desc_text and len(desc_text) > 30:
                    descricao = desc_text[:500]
                    print(f"[OK] Descrição: {len(descricao)} caracteres")
            
            # Fallback: pegar todo o conteúdo da seção
            if descricao == "N/A":
                desc_text = container.get_text(strip=True)
                if len(desc_text) > 100:
                    # Remover o h2 do início
                    desc_text = desc_text.replace("Descrição", "").strip()
                    descricao = desc_text[:500]
        
        dados_produto["descricao"] = descricao
        
        print("[INFO] Scraping concluído com sucesso!")
        logs.append("Scraping concluído com sucesso!")
        
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro na requisição HTTP: {e}")
        logs.append(f"Erro HTTP: {e}")
    except Exception as e:
        print(f"[ERRO] Erro geral durante scraping: {e}")
        logs.append(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()
    
    # Adicionar logs à resposta
    dados_produto["debug_logs"] = logs
    
    return dados_produto


def main():
    """Função principal para executar o scraping."""
    url = "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848"
    
    print("=" * 80)
    print("SCRAPING DE PRODUTO - MERCADO LIVRE (v2.1 - Otimizada)")
    print("=" * 80)
    print()
    
    dados = scrape_mercado_livre(url, capturar_screenshots=False)
    
    print("\n" + "=" * 80)
    print("DADOS EXTRAÍDOS (JSON):")
    print("=" * 80)
    print(json.dumps(dados, ensure_ascii=False, indent=2))
    print("\n")


if __name__ == "__main__":
    main()
