from playwright.sync_api import sync_playwright
import json
import random
import time

def scrape_mercado_livre(url, capturar_screenshots=True):
    """
    Realiza scraping de um produto do Mercado Livre usando Playwright (rápido e leve).
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
        with sync_playwright() as p:
            # Usar Chromium (mais leve que Chrome)
            browser = p.chromium.launch(
                args=["--disable-dev-shm-usage", "--no-sandbox"]
            )
            
            # Criar contexto com user agent aleatório
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            ]
            
            context = browser.new_context(
                user_agent=random.choice(user_agents),
                viewport={"width": 1920, "height": 1080}
            )
            
            page = context.new_page()
            
            print(f"[INFO] Acessando URL: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            
            # Aguardar carregamento
            time.sleep(1)
            
            # EXTRAIR TÍTULO
            try:
                titulo_elem = page.query_selector("h1")
                if titulo_elem:
                    titulo_text = titulo_elem.text_content()
                    if titulo_text:
                        dados_produto["titulo"] = titulo_text.strip()[:200]
                        print(f"[OK] Título: {dados_produto['titulo'][:50]}...")
            except Exception as e:
                print(f"[AVISO] Erro ao extrair título: {e}")
            
            # EXTRAIR BULLET POINTS
            try:
                bullet_elements = page.query_selector_all("span[class*='highlight'], li[class*='bullet'], .ui-pdp-highlights li")
                bullet_points = []
                for elem in bullet_elements[:10]:
                    text = elem.text_content()
                    if text:
                        clean_text = text.strip()
                        if clean_text and len(clean_text) > 10 and len(clean_text) < 300:
                            bullet_points.append(clean_text)
                
                dados_produto["bullet_points"] = list(set(bullet_points))
                if dados_produto["bullet_points"]:
                    print(f"[OK] {len(dados_produto['bullet_points'])} bullet points encontrados")
            except Exception as e:
                print(f"[AVISO] Erro ao extrair bullet points: {e}")
            
            # EXTRAIR CARACTERÍSTICAS
            try:
                table_rows = page.query_selector_all("table tr, div[class*='spec'] tr")
                for row in table_rows:
                    cells = row.query_selector_all("td")
                    if len(cells) >= 2:
                        chave_text = cells[0].text_content()
                        valor_text = cells[1].text_content()
                        
                        if chave_text and valor_text:
                            chave = chave_text.strip()
                            valor = valor_text.strip()
                            if chave and valor:
                                dados_produto["caracteristicas"][chave] = valor
                
                if dados_produto["caracteristicas"]:
                    print(f"[OK] {len(dados_produto['caracteristicas'])} características encontradas")
            except Exception as e:
                print(f"[AVISO] Erro ao extrair características: {e}")
            
            # EXTRAIR COR
            try:
                color_keywords = ['branco', 'preto', 'azul', 'vermelho', 'verde', 'amarelo', 'rosa', 'roxo', 'cinza', 'marrom', 'prata', 'ouro']
                color_elements = page.query_selector_all("span[class*='color'], span[class*='Color'], div[class*='color']")
                
                for elem in color_elements:
                    text = elem.text_content()
                    if text:
                        clean_text = text.lower().strip()
                        if any(keyword in clean_text for keyword in color_keywords) and len(text) < 50:
                            dados_produto["cor"] = text.strip()
                            print(f"[OK] Cor: {dados_produto['cor']}")
                            break
            except Exception as e:
                print(f"[AVISO] Erro ao extrair cor: {e}")
            
            # EXTRAIR DESCRIÇÃO
            try:
                desc_elem = page.query_selector("div[class*='description'], section[class*='description'], article[class*='description']")
                if desc_elem:
                    desc_text = desc_elem.text_content()
                    if desc_text:
                        clean_text = desc_text.strip()
                        if clean_text and len(clean_text) > 30:
                            dados_produto["descricao"] = clean_text[:500]
                            print(f"[OK] Descrição: {len(dados_produto['descricao'])} caracteres")
            except Exception as e:
                print(f"[AVISO] Erro ao extrair descrição: {e}")
            
            browser.close()
            print("[INFO] Scraping concluído com sucesso!")
        
    except Exception as e:
        print(f"[ERRO] Erro geral durante scraping: {e}")
    
    return dados_produto


def main():
    """Função principal para executar o scraping."""
    url = "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848"
    
    print("=" * 80)
    print("SCRAPING DE PRODUTO - MERCADO LIVRE")
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
