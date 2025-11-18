from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import json

def scrape_mercado_livre(url, capturar_screenshots=True):
    """
    Realiza scraping seguro de um produto do Mercado Livre.
    """
    
    dados_produto = {
        "titulo": "N/A",
        "bullet_points": [],
        "caracteristicas": {},
        "cor": "N/A",
        "descricao": "N/A"
    }
    
    driver = None
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"[INFO] Acessando URL: {url}")
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        
        # EXTRAIR TÍTULO
        try:
            titulo_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ui-pdp-title"))
            )
            titulo_text = titulo_element.text
            if titulo_text:
                dados_produto["titulo"] = titulo_text.strip()
        except Exception as e:
            print(f"[AVISO] Erro ao extrair título: {e}")
        
        time.sleep(2)
        
        # EXTRAIR BULLET POINTS
        try:
            bullet_selectors = [
                "ul.andes-list li",
                ".ui-pdp-highlights li",
                ".ui-pdp-description ul li",
                "li[role='listitem']"
            ]
            
            for selector in bullet_selectors:
                try:
                    bullets = driver.find_elements(By.CSS_SELECTOR, selector)
                    if bullets:
                        for bullet in bullets:
                            try:
                                text = bullet.text
                                if text:
                                    clean_text = text.strip()
                                    if clean_text and len(clean_text) > 0:
                                        dados_produto["bullet_points"].append(clean_text)
                            except:
                                continue
                        
                        if dados_produto["bullet_points"]:
                            break
                except:
                    continue
        except Exception as e:
            print(f"[AVISO] Erro ao extrair bullet points: {e}")
        
        # EXTRAIR CARACTERÍSTICAS
        try:
            spec_selectors = [
                "table.andes-table tbody tr",
                "div[class*='attribute-row']",
                "div.ui-pdp-specs"
            ]
            
            for selector in spec_selectors:
                try:
                    spec_rows = driver.find_elements(By.CSS_SELECTOR, selector)
                    if spec_rows:
                        for row in spec_rows:
                            try:
                                cells = row.find_elements(By.TAG_NAME, "td")
                                if len(cells) >= 2:
                                    chave_text = cells[0].text
                                    valor_text = cells[1].text
                                    
                                    if chave_text and valor_text:
                                        chave = chave_text.strip()
                                        valor = valor_text.strip()
                                        
                                        if chave and valor and len(chave) > 0 and len(valor) > 0:
                                            dados_produto["caracteristicas"][chave] = valor
                            except:
                                continue
                        
                        if dados_produto["caracteristicas"]:
                            break
                except:
                    continue
        except Exception as e:
            print(f"[AVISO] Erro ao extrair características: {e}")
        
        # EXTRAIR COR
        try:
            cor_selectors = [
                "span[class*='Color']",
                "span[class*='color']",
                "div[class*='attribute'] span"
            ]
            
            for selector in cor_selectors:
                try:
                    cor_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in cor_elements:
                        try:
                            text = element.text
                            if text:
                                clean_text = text.strip()
                                if clean_text and len(clean_text) > 1 and len(clean_text) < 50 and "%" not in clean_text:
                                    dados_produto["cor"] = clean_text
                                    break
                        except:
                            continue
                    
                    if dados_produto["cor"] != "N/A":
                        break
                except:
                    continue
        except Exception as e:
            print(f"[AVISO] Erro ao extrair cor: {e}")
        
        # EXTRAIR DESCRIÇÃO
        try:
            desc_selectors = [
                "div[class*='description']",
                ".ui-pdp-description",
                ".ui-pdp-long-description"
            ]
            
            for selector in desc_selectors:
                try:
                    desc_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in desc_elements:
                        try:
                            text = element.text
                            if text:
                                clean_text = text.strip()
                                if clean_text and len(clean_text) > 20:
                                    dados_produto["descricao"] = clean_text
                                    break
                        except:
                            continue
                    
                    if dados_produto["descricao"] != "N/A":
                        break
                except:
                    continue
        except Exception as e:
            print(f"[AVISO] Erro ao extrair descrição: {e}")
        
        print("[INFO] Scraping concluído com sucesso!")
        
    except Exception as e:
        print(f"[ERRO] Erro geral durante scraping: {e}")
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
    
    return dados_produto


def main():
    """Função principal para executar o scraping."""
    url = "https://www.mercadolivre.com.br/purificador-de-agua-ibbl-edue-prata-bivolt-79073001/up/MLBU775324063"
    
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
