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
    Realiza scraping de um produto do Mercado Livre e extrai dados estruturados.
    
    Args:
        url (str): URL do produto no Mercado Livre
        capturar_screenshots (bool): Parâmetro aceito mas ignorado por enquanto
        
    Returns:
        dict: Dicionário com os dados extraídos do produto
    """
    
    # Configurar opções do Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em modo headless
    chrome_options.add_argument("--no-sandbox")  # Desabilitar sandbox
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memória
    chrome_options.add_argument("--disable-gpu")  # Desabilitar GPU
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detecção de bot
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Inicializar o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Dicionário para armazenar os dados extraídos
    dados_produto = {
        "titulo": "N/A",
        "bullet_points": [],
        "caracteristicas": {},
        "cor": "N/A",
        "descricao": "N/A"
    }
    
    try:
        print(f"[INFO] Acessando URL: {url}")
        driver.get(url)
        
        # Aguardar carregamento do título principal
        wait = WebDriverWait(driver, 10)
        
        # ===== EXTRAIR TÍTULO =====
        try:
            print("[INFO] Extraindo título...")
            titulo_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ui-pdp-title"))
            )
            dados_produto["titulo"] = titulo_element.text.strip()
            print(f"[OK] Título encontrado: {dados_produto['titulo'][:50]}...")
        except (TimeoutException, NoSuchElementException) as e:
            print(f"[AVISO] Não foi possível extrair o título: {e}")
        
        # Aguardar um pouco para garantir que a página carregou completamente
        time.sleep(3)
        
        # ===== EXTRAIR BULLET POINTS =====
        try:
            print("[INFO] Extraindo bullet points...")
            # Procurar por bullet points em diferentes seletores possíveis
            bullet_selectors = [
                "ul.andes-list li",
                ".ui-pdp-highlights li",
                ".ui-pdp-description ul li",
                "li[role='listitem']"
            ]
            
            for selector in bullet_selectors:
                try:
                    bullets = driver.find_elements(By.CSS_SELECTOR, selector)
                    if bullets and len(bullets) > 0:
                        for bullet in bullets:
                            text = bullet.text.strip()
                            if text and len(text) > 0:
                                dados_produto["bullet_points"].append(text)
                        if dados_produto["bullet_points"]:
                            print(f"[OK] {len(dados_produto['bullet_points'])} bullet points encontrados")
                            break
                except NoSuchElementException:
                    continue
            
            if not dados_produto["bullet_points"]:
                print("[AVISO] Nenhum bullet point encontrado")
        except Exception as e:
            print(f"[AVISO] Erro ao extrair bullet points: {e}")
        
        # ===== EXTRAIR CARACTERÍSTICAS/ESPECIFICAÇÕES =====
        try:
            print("[INFO] Extraindo características...")
            # Procurar pela tabela de especificações
            specs_found = False
            
            # Tenta encontrar a tabela de especificações
            spec_selectors = [
                "table.andes-table tbody tr",
                ".ui-pdp-specs table tbody tr",
                ".ui-pdp-specification tbody tr",
                "tr[data-spec-name]"
            ]
            
            for selector in spec_selectors:
                try:
                    spec_rows = driver.find_elements(By.CSS_SELECTOR, selector)
                    if spec_rows and len(spec_rows) > 0:
                        for row in spec_rows:
                            try:
                                # Tentar extrair chave e valor
                                cells = row.find_elements(By.TAG_NAME, "td")
                                if len(cells) >= 2:
                                    chave = cells[0].text.strip()
                                    valor = cells[1].text.strip()
                                    if chave and valor:
                                        dados_produto["caracteristicas"][chave] = valor
                                        specs_found = True
                            except StaleElementReferenceException:
                                continue
                        
                        if specs_found:
                            print(f"[OK] {len(dados_produto['caracteristicas'])} características encontradas")
                            break
                except NoSuchElementException:
                    continue
            
            if not specs_found:
                print("[AVISO] Nenhuma característica encontrada em tabelas")
        except Exception as e:
            print(f"[AVISO] Erro ao extrair características: {e}")
        
        # ===== EXTRAIR COR =====
        try:
            print("[INFO] Extraindo cor...")
            cor_selectors = [
                "span[class*='color']",
                "div[class*='color'] span",
                ".ui-pdp-color-picker span",
                "div[data-color] span"
            ]
            
            for selector in cor_selectors:
                try:
                    cor_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in cor_elements:
                        text = element.text.strip()
                        if text and len(text) > 0 and len(text) < 50:  # Assumindo que cor tem texto curto
                            dados_produto["cor"] = text
                            print(f"[OK] Cor encontrada: {text}")
                            break
                    if dados_produto["cor"] != "N/A":
                        break
                except NoSuchElementException:
                    continue
            
            if dados_produto["cor"] == "N/A":
                print("[AVISO] Cor não encontrada")
        except Exception as e:
            print(f"[AVISO] Erro ao extrair cor: {e}")
        
        # ===== EXTRAIR DESCRIÇÃO =====
        try:
            print("[INFO] Extraindo descrição...")
            descricao = ""
            
            # Primeiro, tentar extrair de iframe
            try:
                print("[INFO] Procurando por descrição em iframe...")
                # Procurar por iframes
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                print(f"[INFO] {len(iframes)} iframe(s) encontrado(s)")
                
                for idx, iframe in enumerate(iframes):
                    try:
                        driver.switch_to.frame(iframe)
                        print(f"[INFO] Trocando para iframe {idx}...")
                        
                        # Tentar extrair texto do iframe
                        try:
                            descricao_element = driver.find_element(By.CSS_SELECTOR, "body")
                            descricao = descricao_element.text.strip()
                            if descricao and len(descricao) > 20:
                                print(f"[OK] Descrição encontrada em iframe: {len(descricao)} caracteres")
                                break
                        except NoSuchElementException:
                            pass
                        
                        driver.switch_to.default_content()
                    except Exception as e:
                        driver.switch_to.default_content()
                        continue
            except Exception as e:
                print(f"[AVISO] Erro ao processar iframes: {e}")
                driver.switch_to.default_content()
            
            # Se não encontrou em iframe, tentar em divs na página
            if not descricao or len(descricao) < 20:
                try:
                    print("[INFO] Procurando por descrição em elementos da página...")
                    desc_selectors = [
                        ".ui-pdp-description",
                        "div[class*='description']",
                        ".ui-pdp-long-description",
                        "div[data-description]"
                    ]
                    
                    for selector in desc_selectors:
                        try:
                            desc_element = driver.find_element(By.CSS_SELECTOR, selector)
                            text = desc_element.text.strip()
                            if text and len(text) > 20:
                                descricao = text
                                print(f"[OK] Descrição encontrada: {len(descricao)} caracteres")
                                break
                        except NoSuchElementException:
                            continue
                except Exception as e:
                    print(f"[AVISO] Erro ao procurar descrição em elementos: {e}")
            
            dados_produto["descricao"] = descricao if descricao else "N/A"
            
        except Exception as e:
            print(f"[AVISO] Erro ao extrair descrição: {e}")
        
        print("\n[INFO] Scraping concluído com sucesso!")
        
    except TimeoutException:
        print("[ERRO] Timeout ao carregar a página. Verifique a URL ou sua conexão.")
    except NoSuchElementException as e:
        print(f"[ERRO] Elemento não encontrado: {e}")
    except Exception as e:
        print(f"[ERRO] Erro inesperado durante o scraping: {e}")
    
    finally:
        driver.quit()
    
    return dados_produto


def main():
    """Função principal para executar o scraping."""
    
    # URL do produto
    url = "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848?pdp_filters=condition:new%7Cadult_content:yes%7Cofficial_store:399#polycard_client=mshops-appearance-api&component=collection_grid&wid=MLB3928277105&source=eshops&title=Productos+recomendados&tracking_id=c88f48c2-cf79-42ec-b9ae-f0ed50e1633e&sid=storefronts&global_position=12"
    
    print("=" * 80)
    print("SCRAPING DE PRODUTO - MERCADO LIVRE")
    print("=" * 80)
    print()
    
    # Executar scraping
    dados = scrape_mercado_livre(url)
    
    # Exibir resultados
    print("\n" + "=" * 80)
    print("DADOS EXTRAÍDOS:")
    print("=" * 80)
    print(json.dumps(dados, ensure_ascii=False, indent=2))
    print("\n")
    
    # Exibir resumo
    print("=" * 80)
    print("RESUMO:")
    print("=" * 80)
    print(f"Título: {dados['titulo'][:60]}..." if len(dados['titulo']) > 60 else f"Título: {dados['titulo']}")
    print(f"Bullet Points: {len(dados['bullet_points'])} encontrados")
    print(f"Características: {len(dados['caracteristicas'])} encontradas")
    print(f"Cor: {dados['cor']}")
    print(f"Descrição: {len(dados['descricao'])} caracteres")
    print("=" * 80)


if __name__ == "__main__":
    main()
