"""
Script de Web Scraping para Mercado Livre - Versão CLI
Permite extrair dados de produtos passando a URL como argumento
"""

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
import sys
import argparse


def scrape_mercado_livre(url, verbose=True):
    """
    Realiza scraping de um produto do Mercado Livre e extrai dados estruturados.
    
    Args:
        url (str): URL do produto no Mercado Livre
        verbose (bool): Mostrar logs detalhados durante o scraping
        
    Returns:
        dict: Dicionário com os dados extraídos do produto
    """
    
    def log(level, message):
        """Função auxiliar para logging condicional"""
        if verbose:
            print(f"[{level}] {message}")
    
    # Configurar opções do Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
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
        log("INFO", f"Acessando URL: {url}")
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        
        # ===== EXTRAIR TÍTULO =====
        try:
            log("INFO", "Extraindo título...")
            titulo_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ui-pdp-title"))
            )
            dados_produto["titulo"] = titulo_element.text.strip()
            log("OK", f"Título encontrado: {dados_produto['titulo'][:50]}...")
        except (TimeoutException, NoSuchElementException) as e:
            log("AVISO", f"Não foi possível extrair o título")
        
        time.sleep(3)
        
        # ===== EXTRAIR BULLET POINTS =====
        try:
            log("INFO", "Extraindo bullet points...")
            
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
            
            found_bullets = set()
            
            for selector in bullet_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 0:
                        for element in elements:
                            text = element.text.strip()
                            if text and len(text) > 5 and len(text) < 500:
                                found_bullets.add(text)
                        
                        if found_bullets:
                            log("OK", f"Bullet points encontrados com seletor: {selector}")
                            break
                except NoSuchElementException:
                    continue
            
            dados_produto["bullet_points"] = list(found_bullets)
            
            if dados_produto["bullet_points"]:
                log("OK", f"{len(dados_produto['bullet_points'])} bullet points encontrados")
            else:
                log("AVISO", "Nenhum bullet point encontrado")
                
        except Exception as e:
            log("AVISO", f"Erro ao extrair bullet points")
        
        # ===== EXTRAIR CARACTERÍSTICAS/ESPECIFICAÇÕES =====
        try:
            log("INFO", "Extraindo características...")
            
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
                                cells = element.find_elements(By.TAG_NAME, "td")
                                if len(cells) >= 2:
                                    chave = cells[0].text.strip()
                                    valor = cells[1].text.strip()
                                    if chave and valor:
                                        dados_produto["caracteristicas"][chave] = valor
                                        specs_found = True
                                        continue
                                
                                spans = element.find_elements(By.TAG_NAME, "span")
                                if len(spans) >= 2:
                                    chave = spans[0].text.strip()
                                    valor = spans[1].text.strip() if len(spans) > 1 else ""
                                    if chave and valor and not chave.endswith(":"):
                                        dados_produto["caracteristicas"][chave] = valor
                                        specs_found = True
                                        continue
                                
                                text = element.text.strip()
                                if ": " in text or ":" in text:
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
                            log("OK", f"Características encontradas com seletor: {selector}")
                            log("OK", f"{len(dados_produto['caracteristicas'])} características extraídas")
                            break
                            
                except NoSuchElementException:
                    continue
            
            if not specs_found:
                log("AVISO", "Nenhuma característica encontrada")
                
        except Exception as e:
            log("AVISO", f"Erro ao extrair características")
        
        # ===== EXTRAIR COR =====
        try:
            log("INFO", "Extraindo cor...")
            
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
                        if text and 1 < len(text) < 50 and not text.endswith("%") and not re.match(r'^\d+%', text):
                            if "%" not in text:
                                dados_produto["cor"] = text
                                log("OK", f"Cor encontrada: {text}")
                                break
                    
                    if dados_produto["cor"] != "N/A":
                        break
                except NoSuchElementException:
                    continue
            
            if dados_produto["cor"] == "N/A":
                log("AVISO", "Cor não encontrada como campo explícito")
                
        except Exception as e:
            log("AVISO", f"Erro ao extrair cor")
        
        # ===== EXTRAIR DESCRIÇÃO =====
        try:
            log("INFO", "Extraindo descrição...")
            descricao = ""
            
            try:
                log("INFO", "Procurando por descrição em iframe...")
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                log("INFO", f"{len(iframes)} iframe(s) encontrado(s)")
                
                for idx, iframe in enumerate(iframes):
                    try:
                        driver.switch_to.frame(iframe)
                        log("INFO", f"Analisando iframe {idx}...")
                        
                        try:
                            descricao_element = driver.find_element(By.CSS_SELECTOR, "body")
                            descricao = descricao_element.text.strip()
                            if descricao and len(descricao) > 20:
                                log("OK", f"Descrição encontrada em iframe: {len(descricao)} caracteres")
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
                log("AVISO", f"Erro ao processar iframes")
                try:
                    driver.switch_to.default_content()
                except:
                    pass
            
            if not descricao or len(descricao) < 20:
                try:
                    log("INFO", "Procurando por descrição em elementos da página...")
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
                                    log("OK", f"Descrição encontrada: {len(descricao)} caracteres")
                                    break
                            
                            if descricao and len(descricao) > 20:
                                break
                                
                        except NoSuchElementException:
                            continue
                except Exception as e:
                    log("AVISO", f"Erro ao procurar descrição em elementos")
            
            dados_produto["descricao"] = descricao if descricao else "N/A"
            
        except Exception as e:
            log("AVISO", f"Erro ao extrair descrição")
        
        log("INFO", "Scraping concluído com sucesso!")
        
    except TimeoutException:
        log("ERRO", "Timeout ao carregar a página. Verifique a URL ou sua conexão.")
    except NoSuchElementException as e:
        log("ERRO", f"Elemento não encontrado")
    except Exception as e:
        log("ERRO", f"Erro inesperado durante o scraping")
    
    finally:
        driver.quit()
    
    return dados_produto


def main():
    """Função principal para executar o scraping via CLI."""
    
    parser = argparse.ArgumentParser(
        description="Web Scraper para Mercado Livre",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python scraping_cli.py "https://www.mercadolivre.com.br/produto/p/MLB123456"
  python scraping_cli.py "https://www.mercadolivre.com.br/produto/p/MLB123456" --json
  python scraping_cli.py "https://www.mercadolivre.com.br/produto/p/MLB123456" --quiet
        """
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        default="https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
        help="URL do produto no Mercado Livre"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Retornar apenas JSON sem formatação"
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suprimir logs detalhados"
    )
    
    parser.add_argument(
        "--save",
        type=str,
        metavar="ARQUIVO",
        help="Salvar dados em arquivo JSON"
    )
    
    args = parser.parse_args()
    
    # Executar scraping
    verbose = not args.quiet
    dados = scrape_mercado_livre(args.url, verbose=verbose)
    
    # Salvar em arquivo se solicitado
    if args.save:
        try:
            with open(args.save, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            if verbose:
                print(f"\n[INFO] Dados salvos em: {args.save}")
        except Exception as e:
            print(f"[ERRO] Não foi possível salvar arquivo: {e}")
    
    # Exibir resultado
    if args.json:
        print(json.dumps(dados, ensure_ascii=False))
    elif not args.quiet:
        print("\n" + "=" * 80)
        print("DADOS EXTRAÍDOS (JSON):")
        print("=" * 80)
        print(json.dumps(dados, ensure_ascii=False, indent=2))
        print("\n")
        
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
        print(f"\nCor: {dados['cor']}")
        print(f"Descrição: {len(dados['descricao'])} caracteres")
        if dados['descricao'] != "N/A":
            print(f"Primeiros 100 caracteres: {dados['descricao'][:100]}...")
        print("=" * 80)
    else:
        # Modo quiet - apenas retornar JSON
        print(json.dumps(dados, ensure_ascii=False))


if __name__ == "__main__":
    main()
