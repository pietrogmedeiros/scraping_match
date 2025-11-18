# 🛍️ Mercado Livre Scraper API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangelo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.14.1-00A82E?style=flat-square&logo=selenium)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)](https://github.com/pietrogmedeiros/scraping_match)

> 🚀 **API poderosa para scraping automático de produtos do Mercado Livre com captura de screenshots, autenticação por token e suporte total a n8n**

---

## 🔄 Fluxo de Arquitetura (n8n + Servidor Local + ngrok)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            n8n Workflow                                  │
│  (Automação na nuvem - automation.n8n.cloud)                            │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ POST /scrape
                                  │ (URL: https://xxxxx.ngrok-free.app)
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          ngrok Tunnel                                    │
│  (Expõe servidor local para internet)                                   │
│  Command: ngrok http 5000                                               │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Redireciona para
                                  │ localhost:5000
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Flask Server Local (Porta 5000)                      │
│  📍 /scrape (POST)                                                       │
│  - Recebe URL do Mercado Livre                                          │
│  - Valida autenticação (Bearer Token)                                   │
│  - Chama scraper                                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Chama
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              scraping_mercado_livre_v2.py (Selenium)                    │
│  - Abre navegador Chrome headless                                       │
│  - Acessa URL do produto                                               │
│  - Extrai: título, bullets, specs, cor, descrição                       │
│  - Captura 4 screenshots em base64                                      │
│  - Retorna JSON com todos os dados                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Retorna JSON
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    JSON Response + Screenshots                          │
│  {                                                                       │
│    "dados": {                                                            │
│      "titulo": "...",                                                    │
│      "bullet_points": [...],                                            │
│      "caracteristicas": {...},                                          │
│      "screenshots": {                                                    │
│        "pagina_completa": "iVBORw0KGgo...",  ← base64                  │
│        "caracteristicas": "iVBORw0KGgo...",  ← base64                  │
│        "descricao": "iVBORw0KGgo...",        ← base64                  │
│        "rodape": "iVBORw0KGgo..."            ← base64                  │
│      }                                                                   │
│    }                                                                     │
│  }                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ ngrok tunnel retorna
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        n8n Processa Output                              │
│  - Recebe JSON com dados + screenshots                                  │
│  - "Convert to File" → salva PNG                                        │
│  - Pode enviar para S3, email, banco de dados                           │
│  - Executa próximas ações do workflow                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Funcionalidades Principais

### 🎯 Scraping Inteligente
- ✅ Extração automática de **título** do produto
- ✅ Coleta de **bullet points** e vantagens
- ✅ Captura de **características/especificações** com chave-valor
- ✅ Identificação de **cor** (quando disponível)
- ✅ Extração de **descrição completa** (incluindo iframes)
- ✅ Tratamento de **erros robusto**

### 📸 Screenshots Automáticos
Captura automaticamente **5 screenshots** por produto:
1. 🖼️ Página completa do produto
2. 📝 Título e informações principais
3. ⭐ Bullet points/vantagens
4. 🏷️ Tabela de características
5. 📄 Descrição detalhada

### 🔐 Autenticação
- ✅ **Bearer Token** seguro em todos os endpoints
- ✅ Validação em tempo real
- ✅ Suporte a variáveis de ambiente

### 🤖 Integração n8n
- ✅ Documentação completa para n8n
- ✅ Exemplos de 10+ workflows
- ✅ Pronto para automação

### 🌐 Deploy
- ✅ **Vercel** - Deploy em 1 clique
- ✅ **Docker** - Container ready
- ✅ **Local** - Desenvolvimento rápido

### 📊 API RESTful
- ✅ **FastAPI** com documentação Swagger automática
- ✅ **JSON Response** estruturado
- ✅ Tratamento de erros 4xx/5xx
- ✅ CORS configurável

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (n8n/API)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Server                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  POST /scrape (Autenticado)                            │ │
│  │  GET  /status                                          │ │
│  │  GET  /screenshot/{filename}                           │ │
│  │  GET  /screenshots/list                                │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Selenium + Chromium (Headless)                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  1. Navega para URL                                    │ │
│  │  2. Aguarda carregamento                               │ │
│  │  3. Extrai dados (CSS Selectors/XPath)                │ │
│  │  4. Captura 5 screenshots                              │ │
│  │  5. Retorna JSON estruturado                           │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Mercado Livre                              │
│              (Website do Produto)                           │
└─────────────────────────────────────────────────────────────┘
```

### Fluxo de Requisição

```
INPUT (URL)
    │
    ▼
┌─────────────────────────────────────┐
│ 1. Validação de URL                 │
│    - Verifica token                 │
│    - Valida domínio Mercado Livre   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Browser Setup                    │
│    - Inicia Chromium headless       │
│    - Configura user-agent           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Page Load                        │
│    - Navega para URL                │
│    - Aguarda elementos carregarem   │
│    - Timeout 10s                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Data Extraction                  │
│    - Título                         │
│    - Bullet Points                  │
│    - Características                │
│    - Cor                            │
│    - Descrição (iframes)            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 5. Screenshots Capture              │
│    - 5 screenshots diferentes       │
│    - Salvos com timestamp           │
│    - Formato PNG                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 6. Response                         │
│    - JSON estruturado               │
│    - URLs dos screenshots           │
│    - Timestamp                      │
│    - Status de sucesso              │
└──────────────┬──────────────────────┘
               │
               ▼
OUTPUT (JSON Response)
```

---

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11+
- pip ou conda
- Git

### Instalação (5 minutos)

```bash
# 1️⃣ Clonar repositório
git clone https://github.com/pietrogmedeiros/scraping_match.git
cd scraping_match

# 2️⃣ Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou: .venv\Scripts\activate (Windows)

# 3️⃣ Instalar dependências
pip install -r requirements.txt

# 4️⃣ Configurar variáveis de ambiente
cp .env.example .env
# Editar .env e adicionar seu token

# 5️⃣ Iniciar API
python api.py
```

🎉 **API rodando em**: http://localhost:8000

---

## 🤖 Usando com n8n (Automação na Nuvem)

### 1️⃣ Preparar o Servidor Local

```bash
# Terminal 1: Servidor Flask
cd /Users/pietro_medeiros/Downloads/scraping_match
source /Users/pietro_medeiros/.local/share/virtualenvs/pietro_medeiros-XvhqiEUs/bin/activate
python server_local.py

# Terminal 2: ngrok (em outro terminal)
ngrok http 5000
```

Copie a URL gerada pelo ngrok (ex: `https://68a53b5061e1.ngrok-free.app`)

### 2️⃣ Configurar n8n

1. Acesse: https://automation.n8n.cloud
2. Crie um novo workflow
3. Adicione node **"HTTP Request"**:
   - **Method**: POST
   - **URL**: `https://68a53b5061e1.ngrok-free.app/scrape`
   - **Headers**:
     - `Authorization`: `Bearer seu_token`
     - `Content-Type`: `application/json`
   - **Body**:
   ```json
   {
     "url": "https://www.mercadolivre.com.br/...",
     "capturar_screenshots": true
   }
   ```

### 3️⃣ Processar Screenshots

Após HTTP Request, adicione:

**"Execute Code"** (Node.js):
```javascript
const screenshots = $node["HTTP Request"].json.dados.screenshots;
const files = [];

Object.entries(screenshots).forEach(([name, base64]) => {
  files.push({
    name: name,
    data: base64
  });
});

return files;
```

**"Write to File"** (para cada screenshot):
- **File Path**: `/tmp/${name}.png`
- **Input Binary Field**: `data`

### 4️⃣ Opções Avançadas

- **Enviar para S3**: Use node AWS S3
- **Salvar em BD**: PostgreSQL, MongoDB, etc
- **Enviar por Email**: Com anexos PNG
- **Webhook**: Enviar para outra API

---

## 📡 Endpoints

### POST /scrape
```http
POST /scrape
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "url": "https://www.mercadolivre.com.br/...",
  "capturar_screenshots": true
}
```

**Response:**
```json
{
  "sucesso": true,
  "dados": {
    "titulo": "Panificadora 19 Programas Gallant 600w Branca",
    "bullet_points": ["Quantidade de programas:", "..."],
    "caracteristicas": {
      "Capacidade de pão": "1 kg",
      "Quantidade de programas": "19"
    },
    "cor": "Branca",
    "descricao": "Nada melhor do que...",
    "screenshots": {
      "pagina_completa": "/screenshot/20251117_194548_01_pagina_completa.png",
      "titulo": "/screenshot/20251117_194548_02_titulo.png"
    }
  }
}
```

---

## 🔐 Autenticação

Use Bearer Token em todos os endpoints protegidos:

```bash
Authorization: Bearer seu_token_secreto_super_seguro_aqui
```

Gerar token seguro:
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🔗 Integração n8n

### Configuração Básica

1. Adicionar **HTTP Request** node
2. Method: `POST`
3. URL: `http://localhost:8000/scrape`
4. Headers:
   - `Authorization: Bearer seu_token`
   - `Content-Type: application/json`
5. Body:
   ```json
   {
     "url": "https://www.mercadolivre.com.br/...",
     "capturar_screenshots": true
   }
   ```

📖 **Documentação completa**: [N8N_ENDPOINT.md](./N8N_ENDPOINT.md)  
📚 **Workflows prontos**: [N8N_WORKFLOWS.md](./N8N_WORKFLOWS.md)

---

**Versão**: 1.0.0 | **Status**: ✅ Production Ready | **2025**

Feito com ❤️ por Pietro Medeiros

</div>
