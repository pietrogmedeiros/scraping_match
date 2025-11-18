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
    
    dados_produto = {
        "titulo": "N/A",
        "bullet_points": [],
        "caracteristicas": {},
        "cor": "N/A",
        "descricao": "N/A",
        "screenshots": {}
    }
    
    try:
        print(f"[INFO] Acessando URL: {url}")
        
        # Headers realistas para evitar bloqueio
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.mercadolivre.com.br/",
            "Connection": "keep-alive",
            "DNT": "1"
        }
        
        # Fazer requisição
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"[OK] Status: {response.status_code}")
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # ============================================
        # 1. EXTRAIR TÍTULO
        # ============================================
        print("[DEBUG] Extraindo título...")
        h1 = soup.find('h1')
        if h1:
            titulo_text = h1.get_text(strip=True)
            if titulo_text:
                dados_produto["titulo"] = titulo_text[:200]
                print(f"[OK] Título: {dados_produto['titulo'][:50]}...")
        
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
        # 4. EXTRAIR COR
        # ============================================
        print("[DEBUG] Extraindo cor...")
        cor = "N/A"
        
        # Procurar por "Cor:" no texto
        full_text = soup.get_text()
        match = re.search(r'Cor\s*:?\s*([A-Za-záàâãéèêíïóôõöúçñ\s]+?)(?:[,\n\t]|Voltagem|Potência|$)', full_text, re.IGNORECASE)
        if match:
            cor_found = match.group(1).strip()
            # Limpar a cor (remover palavras inúteis)
            palavras_invalidas = ['Escolha', 'Selecione', 'opções', 'produtos', 'veja']
            if not any(p in cor_found.lower() for p in palavras_invalidas) and len(cor_found) < 50:
                cor = cor_found
                print(f"[OK] Cor: {cor}")
        
        dados_produto["cor"] = cor
        
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
        
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro na requisição HTTP: {e}")
    except Exception as e:
        print(f"[ERRO] Erro geral durante scraping: {e}")
        import traceback
        traceback.print_exc()
    
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
