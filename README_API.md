# Mercado Livre Scraper API

API em FastAPI para scraping de produtos do Mercado Livre com autenticação por token.

## Funcionalidades

✅ **Scraping de Produtos** - Extrai título, bullet points, características, cor e descrição  
✅ **Captura de Screenshots** - Captura automática de 5 screenshots por produto  
✅ **Autenticação por Token** - Proteção via Bearer Token  
✅ **Download de Screenshots** - Endpoint para baixar imagens capturadas  
✅ **Limpeza Automática** - Remove screenshots com mais de 7 dias  
✅ **Pronto para Vercel** - Configurado para deployment na Vercel  

## Instalação

### Requisitos
- Python 3.11+
- pip
- Chromium (instalado automaticamente via webdriver-manager)

### Setup Local

```bash
# 1. Clonar/acessar o repositório
cd /Users/pietro_medeiros/Downloads/scrapping-match-1P

# 2. Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
# Editar o arquivo .env e adicionar seu token
cp .env.example .env
# Editar API_TOKEN no arquivo .env
```

## Uso

### Iniciar a API Localmente

```bash
source .venv/bin/activate
python api.py
```

A API estará disponível em: `http://localhost:8000`

### Acessar a Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### 1. Informações da API

```bash
GET /
```

Retorna informações sobre a API e endpoints disponíveis.

**Exemplo:**
```bash
curl http://localhost:8000/
```

### 2. Status da API

```bash
GET /status
```

Verifica se a API está online.

**Exemplo:**
```bash
curl http://localhost:8000/status
```

### 3. Realizar Scraping

```bash
POST /scrape
Authorization: Bearer <seu_token>
Content-Type: application/json

{
  "url": "https://www.mercadolivre.com.br/produto/...",
  "capturar_screenshots": true
}
```

**Parâmetros:**
- `url` (string, obrigatório): URL do produto no Mercado Livre
- `capturar_screenshots` (boolean, opcional): Se deve capturar screenshots (padrão: true)

**Exemplo com cURL:**
```bash
curl -X POST http://localhost:8000/scrape \
  -H "Authorization: Bearer seu_token_secreto_super_seguro_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
    "capturar_screenshots": true
  }'
```

**Exemplo com Python:**
```python
import requests

headers = {
    "Authorization": "Bearer seu_token_secreto_super_seguro_aqui"
}

data = {
    "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
    "capturar_screenshots": True
}

response = requests.post(
    "http://localhost:8000/scrape",
    headers=headers,
    json=data,
    timeout=120
)

print(response.json())
```

**Resposta de Sucesso (200):**
```json
{
  "sucesso": true,
  "mensagem": "Scraping realizado com sucesso",
  "dados": {
    "titulo": "Panificadora 19 Programas Gallant 600w Branca",
    "bullet_points": ["...", "..."],
    "caracteristicas": {
      "Marca": "Gallant",
      "Modelo": "..."
    },
    "cor": "Branca",
    "descricao": "...",
    "screenshots": {
      "pagina_completa": "/screenshot/20251117_193722_01_pagina_completa.png",
      "titulo": "/screenshot/20251117_193722_02_titulo.png",
      "bullet_points": "/screenshot/20251117_193722_03_bullet_points.png",
      "caracteristicas": "/screenshot/20251117_193722_04_caracteristicas.png",
      "descricao": "/screenshot/20251117_193722_05_descricao.png"
    }
  },
  "timestamp": "2025-11-17T19:37:22.123456"
}
```

### 4. Baixar Screenshot

```bash
GET /screenshot/{filename}
Authorization: Bearer <seu_token>
```

Baixa um screenshot capturado.

**Exemplo:**
```bash
curl -H "Authorization: Bearer seu_token_secreto_super_seguro_aqui" \
  http://localhost:8000/screenshot/20251117_193722_01_pagina_completa.png \
  -o pagina_completa.png
```

### 5. Listar Screenshots

```bash
GET /screenshots/list
Authorization: Bearer <seu_token>
```

Lista todos os screenshots disponíveis.

**Exemplo:**
```bash
curl -H "Authorization: Bearer seu_token_secreto_super_seguro_aqui" \
  http://localhost:8000/screenshots/list
```

**Resposta:**
```json
{
  "total": 5,
  "screenshots": [
    {
      "nome": "20251117_193722_01_pagina_completa.png",
      "tamanho_bytes": 123456,
      "url": "/screenshot/20251117_193722_01_pagina_completa.png",
      "data_criacao": "2025-11-17T19:37:22.123456"
    }
  ]
}
```

## Tratamento de Erros

### 401 - Token Inválido ou Ausente

```json
{
  "detail": "Token inválido"
}
```

### 400 - URL Inválida

```json
{
  "detail": "URL deve ser de um produto do Mercado Livre"
}
```

### 404 - Rota Não Encontrada

```json
{
  "erro": "Rota não encontrada",
  "caminho": "/rota/invalida",
  "dica": "Consulte GET / para ver as rotas disponíveis"
}
```

## Testes

Executar suite de testes da API:

```bash
# Certifique-se de que a API está rodando em outro terminal
# python api.py

# Em outro terminal:
python test_api.py
```

Exemplo de saída dos testes:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                   TESTES DA API - MERCADO LIVRE SCRAPER                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

TEST 1: Verificar Status da API
...
✅ PASSOU - Status da API
✅ PASSOU - Informações da API
❌ FALHOU - Scraping sem token
✅ PASSOU - Scraping com token inválido
✅ PASSOU - Scraping com token válido
✅ PASSOU - Listar screenshots

Total: 6/6 testes passaram
```

## Deployment na Vercel

### Pré-requisitos

1. Conta na Vercel (https://vercel.com)
2. Git instalado
3. Repositório no GitHub

### Passos

1. **Fazer push para GitHub:**
```bash
git add .
git commit -m "Adicionar API FastAPI"
git push origin main
```

2. **Conectar no Vercel:**
   - Acessar https://vercel.com/dashboard
   - Clique em "New Project"
   - Selecione seu repositório
   - Vercel detectará automaticamente como projeto Python

3. **Configurar Variáveis de Ambiente:**
   - Na dashboard do Vercel, vá para "Settings" > "Environment Variables"
   - Adicione:
     - `API_TOKEN`: seu_token_secreto_aqui
     - `PORT`: 8000

4. **Deploy:**
   - Clique em "Deploy"
   - Vercel buildará e deployará automaticamente

5. **Acessar API deployada:**
   - URL: `https://seu-projeto.vercel.app`
   - Documentação: `https://seu-projeto.vercel.app/docs`

### Arquivo vercel.json

O arquivo `vercel.json` já está configurado com:
- Build via Python 3.11
- Roteamento correto para FastAPI
- Variáveis de ambiente

## Variáveis de Ambiente

### Arquivo .env

```
# Token de autenticação da API
API_TOKEN=seu_token_secreto_super_seguro_aqui

# Porta padrão
PORT=8000
```

### Vercel

Na Vercel, configure as mesmas variáveis em Settings > Environment Variables.

## Performance e Limitações

- **Timeout**: 120 segundos por scraping
- **Tamanho máximo de Lambda**: 3000MB (para Vercel)
- **Limpeza automática**: Screenshots com > 7 dias são removidos
- **Browser**: Chromium headless para melhor performance

## Segurança

- ✅ Validação de token em todos os endpoints protegidos
- ✅ Validação de URL (apenas Mercado Livre)
- ✅ Sanitização de nomes de arquivo
- ✅ Sem exposição de caminhos internos
- ✅ CORS desabilitado por padrão

## Troubleshooting

### A API não inicia

```bash
# Verificar se as portas estão livres
lsof -i :8000

# Se a porta está ocupada, usar outra
PORT=8001 python api.py
```

### Erro ao fazer scraping

```
TimeoutException: Timeout ao carregar a página
```

Possíveis soluções:
1. Verificar conexão com internet
2. Verificar se a URL é válida
3. Aumentar timeout em `scraping_mercado_livre_v2.py`

### Screenshots não aparecem

1. Verificar se pasta `screenshots/` foi criada
2. Verificar permissões da pasta
3. Verificar espaço em disco

## Arquitetura

```
scrapping-match-1P/
├── api.py                          # API FastAPI
├── scraping_mercado_livre_v2.py    # Lógica de scraping
├── test_api.py                     # Testes
├── vercel.json                     # Configuração Vercel
├── requirements.txt                # Dependências Python
├── .env                            # Variáveis de ambiente
└── screenshots/                    # Screenshots capturados
    └── YYYYMMDD_HHMMSS_*.png
```

## Contribuindo

Para contribuir com melhorias:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## Suporte

Para problemas e dúvidas:
- 📧 Email: seu_email@exemplo.com
- 🐛 Issues: https://github.com/seu-usuario/scrapping-match-1P/issues
- 💬 Discussões: https://github.com/seu-usuario/scrapping-match-1P/discussions

---

**Última atualização:** 17 de novembro de 2025
