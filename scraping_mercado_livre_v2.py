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
import base64
import time


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
    
    # ============================================
    # CAPTURAR SCREENSHOTS (se solicitado)
    # ============================================
    if capturar_screenshots:
        print("[DEBUG] Iniciando captura de screenshots...")
        logs.append("Iniciando captura de screenshots...")
        
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            import time
            
            # Configurar Chrome
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print("[INFO] Abrindo página com Selenium...")
            driver.get(url)
            time.sleep(3)  # Aguardar carregamento
            
            # Capturar screenshots em diferentes partes da página
            screenshots = {}
            
            # 1. Screenshot completo da página
            print("[INFO] Capturando screenshot completo...")
            screenshot_full = driver.get_screenshot_as_png()
            screenshots["pagina_completa"] = base64.b64encode(screenshot_full).decode('utf-8')
            logs.append("✓ Screenshot completo capturado")
            
            # 2. Screenshot do produto (scroll até section principal)
            try:
                product_section = driver.find_element("xpath", "//section[@data-testid='product-section']")
                location = product_section.location
                size = product_section.size
                driver.execute_script(f"window.scrollTo(0, {location['y']});")
                time.sleep(1)
                screenshot_prod = driver.get_screenshot_as_png()
                screenshots["secao_produto"] = base64.b64encode(screenshot_prod).decode('utf-8')
                logs.append("✓ Screenshot da seção de produto capturado")
            except:
                logs.append("⚠ Não foi possível capturar screenshot da seção de produto")
            
            # 3. Screenshot das características
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
                time.sleep(1)
                screenshot_specs = driver.get_screenshot_as_png()
                screenshots["caracteristicas"] = base64.b64encode(screenshot_specs).decode('utf-8')
                logs.append("✓ Screenshot das características capturado")
            except:
                logs.append("⚠ Não foi possível capturar screenshot das características")
            
            # 4. Screenshot da descrição
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
                time.sleep(1)
                screenshot_desc = driver.get_screenshot_as_png()
                screenshots["descricao"] = base64.b64encode(screenshot_desc).decode('utf-8')
                logs.append("✓ Screenshot da descrição capturado")
            except:
                logs.append("⚠ Não foi possível capturar screenshot da descrição")
            
            # 5. Screenshot do rodapé
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                screenshot_footer = driver.get_screenshot_as_png()
                screenshots["rodape"] = base64.b64encode(screenshot_footer).decode('utf-8')
                logs.append("✓ Screenshot do rodapé capturado")
            except:
                logs.append("⚠ Não foi possível capturar screenshot do rodapé")
            
            driver.quit()
            print(f"[OK] {len(screenshots)} screenshots capturados com sucesso!")
            logs.append(f"Total: {len(screenshots)} screenshots capturados")
            dados_produto["screenshots"] = screenshots
            
        except ImportError:
            print("[AVISO] Selenium/webdriver-manager não instalado. Pulando screenshots.")
            logs.append("AVISO: Selenium não disponível - screenshots não capturados")
        except Exception as e:
            print(f"[AVISO] Erro ao capturar screenshots: {e}")
            logs.append(f"AVISO: Erro ao capturar screenshots: {e}")
    
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
