# 📦 Projeto Completo - Mercado Livre Scraper API

## 🎯 Visão Geral

Aplicação Python com FastAPI para scraping de produtos do Mercado Livre com:
- ✅ Extração de dados estruturados (título, características, descrição, etc)
- ✅ Captura automática de 5 screenshots por produto
- ✅ Autenticação por token Bearer
- ✅ API RESTful pronta para produção
- ✅ Pronto para deployment na Vercel
- ✅ Documentação Swagger/OpenAPI automática

## 📁 Estrutura do Projeto

```
scrapping-match-1P/
│
├── 📄 api.py                           # API FastAPI principal
├── 📄 scraping_mercado_livre_v2.py     # Lógica de scraping (otimizada)
├── 📄 scraping_mercado_livre.py        # Versão anterior do scraper
├── 📄 scraping_cli.py                  # Interface CLI (opcional)
├── 📄 test_api.py                      # Suite de testes da API
│
├── 📋 requirements.txt                 # Dependências Python
├── 📋 vercel.json                      # Configuração Vercel
├── 📋 .env                             # Variáveis de ambiente (LOCAL)
├── 📋 .env.example                     # Template de .env
├── 📋 .gitignore                       # Arquivos a ignorar no Git
│
├── 📚 README.md                        # README original
├── 📚 README_API.md                    # Documentação completa da API
├── 📚 EXEMPLOS_USO.md                  # Exemplos em várias linguagens
├── 📚 DEPLOYMENT_VERCEL.md             # Guia de deployment
├── 📚 RESUMO.md                        # Este arquivo
│
└── 📸 screenshots/                     # Screenshots capturados (gerado)
    ├── 20251117_193722_01_pagina_completa.png
    ├── 20251117_193722_02_titulo.png
    ├── 20251117_193722_03_bullet_points.png
    ├── 20251117_193722_04_caracteristicas.png
    └── 20251117_193722_05_descricao.png
```

## 🚀 Quick Start

### 1. Setup Local

```bash
# Clonar e entrar no diretório
cd /Users/pietro_medeiros/Downloads/scrapping-match-1P

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env e adicionar token seguro
```

### 2. Iniciar API

```bash
python api.py
```

API estará disponível em: `http://localhost:8000`

### 3. Testar

```bash
# Em outro terminal
python test_api.py
```

## 📊 Dados Extraídos

Cada scraping retorna um JSON estruturado:

```json
{
  "sucesso": true,
  "mensagem": "Scraping realizado com sucesso",
  "dados": {
    "titulo": "Panificadora 19 Programas Gallant 600w Branca",
    "bullet_points": [
      "Quantidade de programas:",
      "Com janela de visualização:",
      "Capacidade de pão:"
    ],
    "caracteristicas": {
      "Capacidade de pão": "1 kg",
      "Com display digital": "Sim",
      "Quantidade de programas": "19"
    },
    "cor": "Branca",
    "descricao": "Nada melhor do que apreciar o cheiro irresistível...",
    "screenshots": {
      "pagina_completa": "/screenshot/20251117_194548_01_pagina_completa.png",
      "titulo": "/screenshot/20251117_194548_02_titulo.png",
      "bullet_points": "/screenshot/20251117_194548_03_bullet_points.png",
      "caracteristicas": "/screenshot/20251117_194548_04_caracteristicas.png",
      "descricao": "/screenshot/20251117_194548_05_descricao.png"
    }
  },
  "timestamp": "2025-11-17T19:45:48.347050"
}
```

## 🔑 Endpoints Principais

### Informações
```
GET  /              # Info da API
GET  /status        # Status da API
```

### Scraping
```
POST /scrape        # Realizar scraping (requer autenticação)
GET  /screenshot/{filename}  # Baixar screenshot (requer autenticação)
GET  /screenshots/list       # Listar screenshots (requer autenticação)
```

### Documentação
```
GET  /docs          # Swagger UI
GET  /redoc         # ReDoc
GET  /openapi.json  # OpenAPI JSON
```

## 🔐 Autenticação

Todos os endpoints protegidos usam Bearer Token:

```bash
Authorization: Bearer seu_token_secreto_super_seguro_aqui
```

Gerar token seguro:
```python
import secrets
print(secrets.token_urlsafe(32))
```

## 📦 Dependências

| Pacote | Versão | Propósito |
|--------|--------|----------|
| fastapi | 0.104.1 | Framework API |
| uvicorn | 0.24.0 | Servidor ASGI |
| selenium | 4.14.1 | Web scraping/browser |
| webdriver-manager | 4.0.1 | Gerenciar ChromeDriver |
| python-dotenv | 1.0.0 | Variáveis de ambiente |
| pydantic | 2.4.2 | Validação de dados |

## 🧪 Testes

Suite de testes abrangente incluindo:

- ✅ Status da API
- ✅ Informações da API
- ✅ Autenticação (válida/inválida/ausente)
- ✅ Scraping completo
- ✅ Listagem de screenshots
- ✅ Download de screenshots

Resultado esperado: **6/6 testes passando** ✅

## 🌍 Deployment

### Vercel (Recomendado)

```bash
# 1. Push para GitHub
git push origin main

# 2. Conectar Vercel ao repositório
# Vercel → Add New → Project → Import GitHub

# 3. Configurar variáveis de ambiente
# API_TOKEN=seu_token_secreto

# 4. Deploy automático
# Vercel deploy automaticamente a cada push
```

URL da API: `https://seu-projeto.vercel.app`

Mais detalhes em: [DEPLOYMENT_VERCEL.md](./DEPLOYMENT_VERCEL.md)

## 📝 Exemplos de Uso

### Python
```python
import requests

headers = {"Authorization": "Bearer seu_token"}
response = requests.post(
    "http://localhost:8000/scrape",
    headers=headers,
    json={"url": "...", "capturar_screenshots": True},
    timeout=120
)
print(response.json())
```

### cURL
```bash
curl -X POST http://localhost:8000/scrape \
  -H "Authorization: Bearer seu_token" \
  -H "Content-Type: application/json" \
  -d '{"url":"...","capturar_screenshots":true}'
```

### JavaScript
```javascript
const response = await fetch("http://localhost:8000/scrape", {
    method: "POST",
    headers: {
        "Authorization": "Bearer seu_token",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        url: "...",
        capturar_screenshots: true
    })
});
const data = await response.json();
console.log(data);
```

Mais exemplos em: [EXEMPLOS_USO.md](./EXEMPLOS_USO.md)

## 🔍 Features Implementadas

### Scraping
- [x] Extração de título
- [x] Extração de bullet points
- [x] Extração de características/especificações
- [x] Extração de cor
- [x] Extração de descrição (incluindo iframes)
- [x] Captura de 5 screenshots

### API
- [x] Autenticação por token
- [x] Validação de URL
- [x] Tratamento de erros
- [x] Logging detalhado
- [x] Limpeza automática de screenshots antigos
- [x] Documentação Swagger automática

### DevOps
- [x] requirements.txt
- [x] .env e .env.example
- [x] .gitignore
- [x] vercel.json para Vercel
- [x] Docker-ready (adicionar Dockerfile se necessário)

## 📚 Documentação

- **README.md** - Documentação original do projeto
- **README_API.md** - Documentação completa da API
- **EXEMPLOS_USO.md** - Exemplos em 10+ linguagens
- **DEPLOYMENT_VERCEL.md** - Guia passo a passo de deployment
- **RESUMO.md** - Este arquivo

## ⚙️ Configurações Importantes

### Arquivo .env

```env
API_TOKEN=seu_token_secreto_super_seguro_aqui
PORT=8000
```

### Arquivo vercel.json

```json
{
  "version": 2,
  "builds": [{
    "src": "api.py",
    "use": "@vercel/python",
    "config": {
      "maxLambdaSize": "3000mb",
      "runtime": "python3.11"
    }
  }],
  "routes": [{
    "src": "/(.*)",
    "dest": "api.py"
  }]
}
```

## 🎯 Fluxo de Uso

1. **Fazer requisição POST** para `/scrape` com URL e token
2. **API inicia Chromium** em modo headless
3. **Navegador acessa** a URL do Mercado Livre
4. **Extrai dados** estruturados (título, características, etc)
5. **Captura 5 screenshots** em momentos diferentes
6. **Retorna JSON** com todos os dados e URLs dos screenshots
7. **Screenshots armazenados** em `/screenshots`
8. **Limpeza automática** de screenshots com > 7 dias

## 🔔 Performance

| Operação | Tempo | Observações |
|----------|-------|------------|
| Iniciar Chromium | 2-3s | Headless para performance |
| Acessar URL | 2-4s | Depende da conexão |
| Extrair dados | 1-2s | Parallelizado |
| Capturar screenshots | 2-3s | 5 screenshots por produto |
| **Total** | **~10-15s** | Timeout 120s na Vercel |

## 🛡️ Segurança

- ✅ Token de autenticação Bearer
- ✅ Validação de URL (apenas Mercado Livre)
- ✅ Sanitização de nomes de arquivo
- ✅ Sem exposição de caminhos internos
- ✅ Logging seguro sem senhas
- ✅ Variáveis de ambiente para secrets

## 🐛 Troubleshooting

### Erro: "Token inválido"
→ Verificar se o token é o mesmo configurado em `.env` e Vercel

### Erro: "Timeout"
→ Aumentar timeout em `scraping_mercado_livre_v2.py` (máximo 60s na Vercel)

### Erro: "URL inválida"
→ Usar apenas URLs de produtos do Mercado Livre (mercadolivre.com.br)

### Screenshots não aparecem
→ Verificar permissões de pasta `screenshots/` e espaço em disco

## 📈 Roadmap Futuro

- [ ] Adicionar cache de resultados
- [ ] Implementar rate limiting
- [ ] Adicionar autenticação OAuth2
- [ ] Dashboard de analytics
- [ ] Notificações via webhook
- [ ] Suporte a múltiplos idiomas
- [ ] API GraphQL
- [ ] Websockets para atualizações em tempo real

## 🤝 Contribuindo

1. Fork o repositório
2. Criar branch (`git checkout -b feature/nova-feature`)
3. Commit mudanças (`git commit -am 'Add nova feature'`)
4. Push (`git push origin feature/nova-feature`)
5. Pull Request

## 📞 Suporte

- 📧 Email: seu_email@exemplo.com
- 🐛 Issues: GitHub Issues
- 💬 Discussões: GitHub Discussions
- 📖 Docs: Consultar README_API.md

## 📄 Licença

MIT License - Veja LICENSE para mais detalhes

## ✨ Créditos

- **Framework**: FastAPI
- **Scraping**: Selenium
- **Browser**: Chromium
- **Deployment**: Vercel

## 📊 Estatísticas

- **Arquivos Python**: 4
- **Documentação**: 4 arquivos
- **Dependências**: 6 pacotes
- **Endpoints**: 6 (3 protegidos)
- **Testes**: 6 cases
- **Screenshots por produto**: 5
- **Tempo médio**: 10-15s por produto

---

**Status**: ✅ Pronto para Produção
**Última atualização**: 17 de novembro de 2025
**Versão**: 1.0.0
