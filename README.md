# 🛍️ Mercado Livre Scraper API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangelo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.14.1-00A82E?style=flat-square&logo=selenium)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)](https://github.com/pietrogmedeiros/scraping_match)

> 🚀 **API poderosa para scraping automático de produtos do Mercado Livre com captura de screenshots, autenticação por token e suporte total a n8n**

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

## 📦 Deploy

### Vercel (Recomendado)

```bash
# 1. Push para GitHub
git push origin main

# 2. Conectar Vercel
# Vercel → Add New → Project → Import GitHub

# 3. Configurar variáveis
# API_TOKEN=seu_token_secreto
```

✅ API em: `https://seu-projeto.vercel.app`

---

## 📚 Documentação

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
3. **Desabilitar GPU**: Reduz consumo de memória| **README.md** | Este arquivo (Visão geral) |
| **[README_API.md](./README_API.md)** | Documentação completa da API |
| **[N8N_ENDPOINT.md](./N8N_ENDPOINT.md)** | Guia de configuração no n8n |
| **[N8N_WORKFLOWS.md](./N8N_WORKFLOWS.md)** | 10+ exemplos de workflows |
| **[EXEMPLOS_USO.md](./EXEMPLOS_USO.md)** | Exemplos em 10+ linguagens |
| **[DEPLOYMENT_VERCEL.md](./DEPLOYMENT_VERCEL.md)** | Guia completo de deploy |
| **[RESUMO.md](./RESUMO.md)** | Overview técnico do projeto |

---

## ⚙️ Configuração

### Arquivo `.env`

```env
API_TOKEN=seu_token_secreto_super_seguro_aqui
PORT=8000
```

---

## 🧪 Testes

```bash
python test_api.py
```

**Resultado esperado**: ✅ 6/6 testes passando

---

## 📈 Performance

| Operação | Tempo |
|----------|-------|
| Iniciar Chromium | 2-3s |
| Acessar URL | 2-4s |
| Extrair dados | 1-2s |
| Capturar screenshots | 2-3s |
| **Total** | **~10-15s** |

---

## 📦 Dependências

```
fastapi==0.104.1          # Framework API
uvicorn==0.24.0           # Servidor ASGI
selenium==4.14.1          # Web scraping
webdriver-manager==4.0.1  # Gerenciar drivers
python-dotenv==1.0.0      # Variáveis de ambiente
pydantic==2.4.2           # Validação de dados
requests==2.31.0          # HTTP client
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

- 📖 [Documentação Completa](./README_API.md)
- 🐛 [GitHub Issues](https://github.com/pietrogmedeiros/scraping_match/issues)
- 💬 [GitHub Discussions](https://github.com/pietrogmedeiros/scraping_match/discussions)

---

## ⭐ Dê uma estrela!

Se este projeto foi útil, considere dar uma ⭐

---

<div align="center">

### 🚀 Pronto para começar?

[📖 Documentação](./README_API.md) | [🔧 n8n](./N8N_ENDPOINT.md) | [🌐 Deploy](./DEPLOYMENT_VERCEL.md)

**Versão**: 1.0.0 | **Status**: ✅ Production Ready | **2025**

Made with ❤️

</div>
