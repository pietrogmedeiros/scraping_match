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
import re
import os
from datetime import datetime

def scrape_mercado_livre(url, capturar_screenshots=True):
    """
    Realiza scraping de um produto do Mercado Livre e extrai dados estruturados.
    
    Args:
        url (str): URL do produto no Mercado Livre
        capturar_screenshots (bool): Se True, captura screenshots durante o scraping
        
    Returns:
        dict: Dicionário com os dados extraídos do produto (inclui caminho das screenshots se capturadas)
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
    
    # Criar diretório para screenshots se necessário
    screenshots_dir = "screenshots"
    if capturar_screenshots and not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
        print(f"[INFO] Diretório '{screenshots_dir}' criado")
    
    # Timestamp para identificar a execução
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Inicializar o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Dicionário para armazenar os dados extraídos
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
        driver.get(url)
        
        # Aguardar carregamento do título principal
        wait = WebDriverWait(driver, 10)
        
        # Capturar screenshot da página completa no início
        if capturar_screenshots:
            screenshot_path = os.path.join(screenshots_dir, f"{timestamp}_01_pagina_completa.png")
            driver.save_screenshot(screenshot_path)
            dados_produto["screenshots"]["pagina_completa"] = screenshot_path
            print(f"[OK] Screenshot da página capturado: {screenshot_path}")
        
        # ===== EXTRAIR TÍTULO =====
        try:
            print("[INFO] Extraindo título...")
            titulo_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ui-pdp-title"))
            )
            dados_produto["titulo"] = titulo_element.text.strip()
            print(f"[OK] Título encontrado: {dados_produto['titulo'][:50]}...")
            
            # Capturar screenshot do título
            if capturar_screenshots:
                screenshot_path = os.path.join(screenshots_dir, f"{timestamp}_02_titulo.png")
                titulo_element.screenshot(screenshot_path)
                dados_produto["screenshots"]["titulo"] = screenshot_path
                print(f"[OK] Screenshot do título capturado: {screenshot_path}")
        except (TimeoutException, NoSuchElementException) as e:
            print(f"[AVISO] Não foi possível extrair o título: {e}")
        
        # Aguardar um pouco para garantir que a página carregou completamente
        time.sleep(3)
        
        # ===== EXTRAIR BULLET POINTS =====
        try:
            print("[INFO] Extraindo bullet points...")
            
            # Procurar especificamente na seção de highlights/vantagens
            bullet_selectors = [
                "span[class*='highlight']",
                "div[class*='highlight'] span",
                "li[class*='highlight']",
                "div.ui-pdp-highlights li",
                "ul.andes-list li",
                "ul li span",
                "li[role='listitem']",
                "div[class*='feature'] span"
            ]
            
            found_bullets = set()  # Usar set para evitar duplicatas
            
            for selector in bullet_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 0:
                        for element in elements:
                            text = element.text.strip()
                            if text and len(text) > 5 and len(text) < 500:  # Filtrar textos válidos
                                found_bullets.add(text)
                        
                        if found_bullets:
                            print(f"[OK] Bullet points encontrados com seletor: {selector}")
                            break
                except NoSuchElementException:
                    continue
            
            dados_produto["bullet_points"] = list(found_bullets)
            
            if dados_produto["bullet_points"]:
                print(f"[OK] {len(dados_produto['bullet_points'])} bullet points encontrados")
                
                # Capturar screenshot dos bullet points
                if capturar_screenshots:
                    try:
                        for selector in bullet_selectors:
                            try:
                                highlight_elem = driver.find_element(By.CSS_SELECTOR, selector)
                                screenshot_path = os.path.join(screenshots_dir, f"{timestamp}_03_bullet_points.png")
                                highlight_elem.screenshot(screenshot_path)
                                dados_produto["screenshots"]["bullet_points"] = screenshot_path
                                print(f"[OK] Screenshot dos bullet points capturado: {screenshot_path}")
                                break
                            except:
                                continue
                    except Exception as e:
                        print(f"[AVISO] Não foi possível capturar screenshot dos bullet points: {e}")
            else:
                print("[AVISO] Nenhum bullet point encontrado")
                
        except Exception as e:
            print(f"[AVISO] Erro ao extrair bullet points: {e}")
        
        # ===== EXTRAIR CARACTERÍSTICAS/ESPECIFICAÇÕES =====
        try:
            print("[INFO] Extraindo características...")
            
            # Procurar por elementos de especificação
            spec_selectors = [
                "div[class*='attribute-row']",
                "div[class*='attribute']",
                "div.ui-pdp-specs",
                "table.andes-table tbody tr",
                "div[data-spec-name]",
                "div[class*='spec']",
                "li[class*='attribute']"
            ]
            
            specs_found = False
            
            for selector in spec_selectors:
                try:
                    spec_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if spec_elements and len(spec_elements) > 0:
                        for element in spec_elements:
                            try:
                                # Tentar diferentes padrões de chave-valor
                                
                                # Padrão 1: dois td/spans em sequência
                                cells = element.find_elements(By.TAG_NAME, "td")
                                if len(cells) >= 2:
                                    chave = cells[0].text.strip()
                                    valor = cells[1].text.strip()
                                    if chave and valor:
                                        dados_produto["caracteristicas"][chave] = valor
                                        specs_found = True
                                        continue
                                
                                # Padrão 2: Chave e valor em spans dentro de divs
                                spans = element.find_elements(By.TAG_NAME, "span")
                                if len(spans) >= 2:
                                    chave = spans[0].text.strip()
                                    valor = spans[1].text.strip() if len(spans) > 1 else ""
                                    if chave and valor and not chave.endswith(":"):
                                        dados_produto["caracteristicas"][chave] = valor
                                        specs_found = True
                                        continue
                                
                                # Padrão 3: Elemento com classe de rótulo e valor
                                text = element.text.strip() if element.text else ""
                                if text and (": " in text or ":" in text):
                                    partes = text.split(":", 1)
                                    if len(partes) == 2:
                                        chave = partes[0].strip()
                                        valor = partes[1].strip()
                                        if chave and valor:
                                            dados_produto["caracteristicas"][chave] = valor
                                            specs_found = True
                                
                            except (StaleElementReferenceException, NoSuchElementException):
                                continue
                        
                        if specs_found:
                            print(f"[OK] Características encontradas com seletor: {selector}")
                            print(f"[OK] {len(dados_produto['caracteristicas'])} características extraídas")
                            
                            # Capturar screenshot das características
                            if capturar_screenshots:
                                try:
                                    spec_container = driver.find_element(By.CSS_SELECTOR, selector)
                                    screenshot_path = os.path.join(screenshots_dir, f"{timestamp}_04_caracteristicas.png")
                                    spec_container.screenshot(screenshot_path)
                                    dados_produto["screenshots"]["caracteristicas"] = screenshot_path
                                    print(f"[OK] Screenshot das características capturado: {screenshot_path}")
                                except Exception as e:
                                    print(f"[AVISO] Não foi possível capturar screenshot das características: {e}")
                            break
                            
                except NoSuchElementException:
                    continue
            
            if not specs_found:
                print("[AVISO] Nenhuma característica encontrada")
                
        except Exception as e:
            print(f"[AVISO] Erro ao extrair características: {e}")
        
        # ===== EXTRAIR COR =====
        try:
            print("[INFO] Extraindo cor...")
            
            cor_selectors = [
                "span[class*='Color']",
                "span[class*='color']",
                "div[class*='attribute'] span:nth-child(2)",
                "li[class*='color'] span",
                "div[data-attribute-name='color'] span",
                "button[class*='color']"
            ]
            
            for selector in cor_selectors:
                try:
                    elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elementos:
                        text = element.text.strip()
                        # Filtrar por comprimento e evitar números de desconto
                        if text and 1 < len(text) < 50 and not text.endswith("%") and not re.match(r'^\d+%', text):
                            # Verificar se não é um valor de desconto ou percentual
                            if "%" not in text:
                                dados_produto["cor"] = text
                                print(f"[OK] Cor encontrada: {text}")
                                break
                    
                    if dados_produto["cor"] != "N/A":
                        break
                except NoSuchElementException:
                    continue
            
            if dados_produto["cor"] == "N/A":
                print("[AVISO] Cor não encontrada como campo explícito")
                
        except Exception as e:
            print(f"[AVISO] Erro ao extrair cor: {e}")
        
        # ===== EXTRAIR DESCRIÇÃO =====
        try:
            print("[INFO] Extraindo descrição...")
            descricao = ""
            
            # Primeiro, tentar extrair de iframe
            try:
                print("[INFO] Procurando por descrição em iframe...")
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                print(f"[INFO] {len(iframes)} iframe(s) encontrado(s)")
                
                for idx, iframe in enumerate(iframes):
                    try:
                        driver.switch_to.frame(iframe)
                        print(f"[INFO] Analisando iframe {idx}...")
                        
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
                        try:
                            driver.switch_to.default_content()
                        except:
                            pass
                        continue
                        
            except Exception as e:
                print(f"[AVISO] Erro ao processar iframes: {e}")
                try:
                    driver.switch_to.default_content()
                except:
                    pass
            
            # Se não encontrou em iframe, tentar em divs na página
            if not descricao or len(descricao) < 20:
                try:
                    print("[INFO] Procurando por descrição em elementos da página...")
                    desc_selectors = [
                        "div[class*='description']",
                        ".ui-pdp-description",
                        ".ui-pdp-long-description",
                        "div[data-description]",
                        "article[class*='description']",
                        "section[class*='description']"
                    ]
                    
                    for selector in desc_selectors:
                        try:
                            desc_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            for element in desc_elements:
                                text = element.text.strip()
                                if text and len(text) > 20:
                                    descricao = text
                                    print(f"[OK] Descrição encontrada: {len(descricao)} caracteres")
                                    break
                            
                            if descricao and len(descricao) > 20:
                                break
                                
                        except NoSuchElementException:
                            continue
                except Exception as e:
                    print(f"[AVISO] Erro ao procurar descrição em elementos: {e}")
            
            dados_produto["descricao"] = descricao if descricao else "N/A"
            
            # Capturar screenshot da descrição
            if capturar_screenshots and dados_produto["descricao"] != "N/A":
                try:
                    desc_selectors_screenshot = [
                        "div[class*='description']",
                        ".ui-pdp-description",
                        ".ui-pdp-long-description",
                        "article[class*='description']"
                    ]
                    for selector in desc_selectors_screenshot:
                        try:
                            desc_elem = driver.find_element(By.CSS_SELECTOR, selector)
                            screenshot_path = os.path.join(screenshots_dir, f"{timestamp}_05_descricao.png")
                            desc_elem.screenshot(screenshot_path)
                            dados_produto["screenshots"]["descricao"] = screenshot_path
                            print(f"[OK] Screenshot da descrição capturado: {screenshot_path}")
                            break
                        except:
                            continue
                except Exception as e:
                    print(f"[AVISO] Não foi possível capturar screenshot da descrição: {e}")
            
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
    url = "https://www.mercadolivre.com.br/purificador-de-agua-ibbl-edue-prata-bivolt-79073001/up/MLBU775324063"
    
    print("=" * 80)
    print("SCRAPING DE PRODUTO - MERCADO LIVRE")
    print("=" * 80)
    print()
    
    # Executar scraping com captura de screenshots
    dados = scrape_mercado_livre(url, capturar_screenshots=True)
    
    # Exibir resultados
    print("\n" + "=" * 80)
    print("DADOS EXTRAÍDOS (JSON):")
    print("=" * 80)
    print(json.dumps(dados, ensure_ascii=False, indent=2))
    print("\n")
    
    # Exibir resumo
    print("=" * 80)
    print("RESUMO:")
    print("=" * 80)
    print(f"Título: {dados['titulo'][:60]}..." if len(dados['titulo']) > 60 else f"Título: {dados['titulo']}")
    print(f"Bullet Points: {len(dados['bullet_points'])} encontrados")
    if dados['bullet_points']:
        for i, bp in enumerate(dados['bullet_points'], 1):
            print(f"  {i}. {bp[:60]}...")
    print(f"\nCaracterísticas: {len(dados['caracteristicas'])} encontradas")
    if dados['caracteristicas']:
        for chave, valor in dados['caracteristicas'].items():
            print(f"  - {chave}: {valor}")
    print(f"Cor: {dados['cor']}")
    print(f"Descrição: {len(dados['descricao'])} caracteres")
    if dados['descricao'] != "N/A":
        print(f"Primeiros 100 caracteres: {dados['descricao'][:100]}...")
    
    # Exibir informações sobre screenshots capturados
    if dados['screenshots']:
        print(f"\nScreenshots capturados: {len(dados['screenshots'])}")
        for tipo, caminho in dados['screenshots'].items():
            print(f"  - {tipo}: {caminho}")
    
    print("=" * 80)


if __name__ == "__main__":
    main()
