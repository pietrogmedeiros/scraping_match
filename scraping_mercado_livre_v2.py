import requests
from bs4 import BeautifulSoup
import json
import random

def scrape_mercado_livre(url, capturar_screenshots=True):
    """
    Realiza scraping leve de um produto do Mercado Livre usando BeautifulSoup.
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
        # User-agents para não parecer bot
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        print(f"[INFO] Acessando URL: {url}")
        
        # Fazer requisição com timeout curto
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # EXTRAIR TÍTULO
        try:
            titulo_elem = soup.find(['h1', 'h2'])
            if titulo_elem:
                titulo_text = titulo_elem.get_text(strip=True)
                if titulo_text and len(titulo_text) > 5:
                    dados_produto["titulo"] = titulo_text[:200]
                    print(f"[OK] Título: {dados_produto['titulo'][:50]}...")
        except Exception as e:
            print(f"[AVISO] Erro ao extrair título: {e}")
        
        # EXTRAIR BULLET POINTS
        try:
            bullet_points = []
            
            selectors = [
                ('span', {'class': lambda x: x and 'highlight' in str(x).lower()}),
                ('li', {}),
                ('div', {'class': lambda x: x and 'bullet' in str(x).lower()})
            ]
            
            for tag, attrs in selectors:
                elements = soup.find_all(tag, attrs, limit=20)
                for elem in elements:
                    text = elem.get_text(strip=True)
                    if text and len(text) > 10 and len(text) < 300:
                        bullet_points.append(text)
                
                if len(bullet_points) > 3:
                    break
            
            dados_produto["bullet_points"] = list(set(bullet_points))[:10]
            if dados_produto["bullet_points"]:
                print(f"[OK] {len(dados_produto['bullet_points'])} bullet points encontrados")
        except Exception as e:
            print(f"[AVISO] Erro ao extrair bullet points: {e}")
        
        # EXTRAIR CARACTERÍSTICAS
        try:
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        chave = cells[0].get_text(strip=True)
                        valor = cells[1].get_text(strip=True)
                        if chave and valor and len(chave) > 0 and len(valor) > 0:
                            dados_produto["caracteristicas"][chave] = valor
            
            if dados_produto["caracteristicas"]:
                print(f"[OK] {len(dados_produto['caracteristicas'])} características encontradas")
        except Exception as e:
            print(f"[AVISO] Erro ao extrair características: {e}")
        
        # EXTRAIR COR
        try:
            color_keywords = ['branco', 'preto', 'azul', 'vermelho', 'verde', 'amarelo', 'rosa', 'roxo', 'cinza', 'marrom', 'prata', 'ouro', 'white', 'black', 'blue', 'red', 'green']
            
            for text_elem in soup.find_all(['span', 'div', 'p']):
                text = text_elem.get_text(strip=True).lower()
                if any(keyword in text for keyword in color_keywords) and len(text) < 50:
                    dados_produto["cor"] = text_elem.get_text(strip=True)
                    print(f"[OK] Cor: {dados_produto['cor']}")
                    break
        except Exception as e:
            print(f"[AVISO] Erro ao extrair cor: {e}")
        
        # EXTRAIR DESCRIÇÃO
        try:
            desc_elem = soup.find(['article', 'section', 'div'], {'class': lambda x: x and 'description' in str(x).lower()})
            if desc_elem:
                descricao_text = desc_elem.get_text(strip=True)
                if descricao_text and len(descricao_text) > 30:
                    dados_produto["descricao"] = descricao_text[:500]
                    print(f"[OK] Descrição: {len(dados_produto['descricao'])} caracteres")
        except Exception as e:
            print(f"[AVISO] Erro ao extrair descrição: {e}")
        
        print("[INFO] Scraping concluído com sucesso!")
        
    except requests.Timeout:
        print("[ERRO] Timeout ao acessar a página")
    except requests.RequestException as e:
        print(f"[ERRO] Erro na requisição: {e}")
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
