# Mercado Livre Web Scraper

Script Python de web scraping para extrair dados estruturados de produtos do Mercado Livre utilizando Selenium com navegador Chromium em modo headless.

## 📋 Características

✅ **Extração de Dados Estruturados:**
- Título do produto
- Bullet points/vantagens do produto
- Características e especificações (chave-valor)
- Cor do produto
- Descrição completa (com suporte a iframes)

✅ **Tecnologias:**
- Selenium WebDriver para automação do navegador
- Chromium em modo headless para melhor performance
- Webdriver-manager para gerenciar automaticamente o driver
- Tratamento robusto de exceções
- Seletores CSS/XPath otimizados

✅ **Recursos Avançados:**
- Espera explícita para carregamento de elementos
- Suporte a iframes com troca de contexto
- Múltiplos seletores para aumentar compatibilidade
- Remoção de duplicatas em dados extraídos
- Logging detalhado do processo de scraping

## 📦 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Navegar até o diretório do projeto:**
```bash
cd /Users/pietro_medeiros/Downloads/scrapping-match-1P
```

2. **Instalar dependências:**
```bash
pip install selenium webdriver-manager
```

Ou, se estiver usando um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No macOS/Linux
pip install selenium webdriver-manager
```

## 🚀 Uso

### Executar o Script Principal

```bash
python scraping_mercado_livre.py
```

Ou a versão v2 (com mais extração de dados):
```bash
python scraping_mercado_livre_v2.py
```

### Exemplo de Saída

```json
{
  "titulo": "Panificadora 19 Programas Gallant 600w Branca",
  "bullet_points": [
    "Quantidade de programas:",
    "Capacidade de pão:"
  ],
  "caracteristicas": {
    "Capacidade de pão": "1 kg",
    "Quantidade de programas": "19"
  },
  "cor": "Branco",
  "descricao": "Descrição\nNada melhor do que apreciar o cheiro irresistível de pão fresca..."
}
```

## 🔧 Como Customizar para Outros Produtos

### Método 1: Modificar a URL no Script
Edite a variável `url` na função `main()`:

```python
def main():
    url = "NOVA_URL_DO_PRODUTO_AQUI"
    dados = scrape_mercado_livre(url)
```

### Método 2: Passar URL como Argumento
Modifique o script para aceitar argumentos:

```python
import sys

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "URL_PADRÃO"
    dados = scrape_mercado_livre(url)

if __name__ == "__main__":
    main()
```

Uso:
```bash
python scraping_mercado_livre.py "https://seu-link-aqui.com"
```

## 📊 Estrutura de Dados Retornada

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `titulo` | string | Título completo do produto |
| `bullet_points` | list | Lista de vantagens/destaques |
| `caracteristicas` | dict | Dicionário chave-valor das especificações |
| `cor` | string | Cor do produto ou "N/A" |
| `descricao` | string | Descrição completa do produto |

## ⚙️ Configurações Avançadas

### Ajustar Timeout
No script, modifique a linha:
```python
wait = WebDriverWait(driver, 10)  # 10 segundos
```

### Desabilitar Modo Headless
Para ver o navegador em ação, comente a linha:
```python
# chrome_options.add_argument("--headless")
```

### Adicionar Tempo de Espera Extra
Para páginas mais lentas, aumente:
```python
time.sleep(3)  # Aumentar para 5 ou mais se necessário
```

## 🐛 Tratamento de Erros

O script inclui tratamento para:
- **TimeoutException**: Página não carrega no tempo limite
- **NoSuchElementException**: Elemento não encontrado na página
- **StaleElementReferenceException**: Elemento desatualizado no DOM
- **Erros genéricos**: Exceções não previstas

Todos os erros são capturados e registrados, permitindo que o script continue a execução mesmo com falhas parciais.

## 📝 Logging

O script fornece feedback detalhado em tempo real:
- `[INFO]` - Operações informativas
- `[OK]` - Sucesso na extração
- `[AVISO]` - Problemas não críticos (dados não encontrados)
- `[ERRO]` - Erros críticos

## 🔒 Considerações de Performance e Segurança

1. **Modo Headless**: Melhora a performance significativamente
2. **User-Agent Customizado**: Evita detecção como bot
3. **Desabilitar GPU**: Reduz consumo de memória
4. **Desabilitar Sandbox**: Necessário em alguns ambientes
5. **Timeout Apropriado**: Evita travamentos indefinidos

## 🤝 Integração com Outros Projetos

```python
from scraping_mercado_livre import scrape_mercado_livre

url = "https://seu-produto.com"
dados = scrape_mercado_livre(url)

# Usar os dados
print(f"Produto: {dados['titulo']}")
print(f"Preço no: {dados.get('preco', 'N/A')}")
```

## ⚠️ Disclaimer

Este script é fornecido apenas para fins educacionais. Certifique-se de:
- Verificar os termos de serviço do Mercado Livre
- Respeitar o arquivo `robots.txt`
- Não sobrecarregar os servidores
- Usar responsavelmente e eticamente

## 📚 Recursos Adicionais

- [Documentação Selenium](https://selenium-python.readthedocs.io/)
- [Webdriver-manager](https://github.com/SherlocksoftWare/python-webdriver-manager)
- [MDN - Seletores CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [W3C XPath](https://www.w3.org/TR/xpath-10/)

## 📞 Suporte

Se encontrar problemas:
1. Verifique se as dependências estão instaladas: `pip list`
2. Verifique a conexão com a internet
3. Confirme se a URL do produto é válida
4. Tente aumentar o timeout em `WebDriverWait`
5. Verifique se o Chromium foi instalado corretamente

## 📄 Licença

Este projeto é fornecido como está, sem garantias.
