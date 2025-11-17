# 🔄 Workflows n8n - Exemplos Prontos

## Workflow 1: Scraping Simples

Este é o workflow mais básico para fazer um scraping de um produto.

### JSON Export

```json
{
  "name": "Mercado Livre Scraper - Simples",
  "nodes": [
    {
      "parameters": {},
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/scrape",
        "headers": {
          "Authorization": "Bearer seu_token_secreto_super_seguro_aqui",
          "Content-Type": "application/json"
        },
        "body": {
          "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
          "capturar_screenshots": true
        }
      },
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 300]
    },
    {
      "parameters": {
        "keepOnlySet": false,
        "values": {
          "string": [
            {
              "name": "titulo",
              "value": "=<$node[\"HTTP Request\"].json.dados.titulo"
            },
            {
              "name": "bullet_points",
              "value": "=<$node[\"HTTP Request\"].json.dados.bullet_points"
            },
            {
              "name": "caracteristicas",
              "value": "=<$node[\"HTTP Request\"].json.dados.caracteristicas"
            },
            {
              "name": "screenshots",
              "value": "=<$node[\"HTTP Request\"].json.dados.screenshots"
            }
          ]
        }
      },
      "name": "Extract Data",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Start": {
      "main": [[{ "node": "HTTP Request", "branch": 0, "index": 0 }]]
    },
    "HTTP Request": {
      "main": [[{ "node": "Extract Data", "branch": 0, "index": 0 }]]
    }
  }
}
```

---

## Workflow 2: Scraping com Tratamento de Erros

Inclui validação e tratamento de erros.

### Passos

1. **Start** - Trigger manual
2. **HTTP Request** - POST /scrape
3. **IF** - Verificar se sucesso
4. **Success Path** - Salvar dados
5. **Error Path** - Enviar notificação

### Código do IF

```javascript
// Verificar se o scraping foi bem-sucedido
{{ $node["HTTP Request"].json.sucesso === true }}
```

---

## Workflow 3: Scraping em Lote

Para fazer scraping de múltiplos produtos.

### Configuração

1. **Trigger**: Pega lista de URLs de um banco de dados ou JSON
2. **Loop**: Itera sobre cada URL
3. **HTTP Request**: Faz scraping de cada produto
4. **Save**: Salva resultados

### Pseudocódigo

```javascript
// Em um "Function" node
const urls = [
  "https://www.mercadolivre.com.br/produto1",
  "https://www.mercadolivre.com.br/produto2",
  "https://www.mercadolivre.com.br/produto3"
];

return urls.map(url => ({
  url: url,
  capturar_screenshots: true
}));
```

---

## Workflow 4: Scraping com Salvamento em Banco de Dados

Salva os dados em um banco de dados.

### Passos

```
HTTP Request (POST /scrape)
        ↓
    IF (sucesso)
        ↓
    Set (Preparar dados)
        ↓
    MongoDB/PostgreSQL (Inserir)
        ↓
    Notification (Sucesso)
```

### Set Node Configuration

```json
{
  "product_data": {
    "titulo": "{{ $node[\"HTTP Request\"].json.dados.titulo }}",
    "bullet_points": "{{ $node[\"HTTP Request\"].json.dados.bullet_points }}",
    "caracteristicas": "{{ $node[\"HTTP Request\"].json.dados.caracteristicas }}",
    "cor": "{{ $node[\"HTTP Request\"].json.dados.cor }}",
    "descricao": "{{ $node[\"HTTP Request\"].json.dados.descricao }}",
    "screenshots": "{{ $node[\"HTTP Request\"].json.dados.screenshots }}",
    "timestamp": "{{ $node[\"HTTP Request\"].json.timestamp }}",
    "data_insercao": "{{ new Date().toISOString() }}"
  }
}
```

---

## Workflow 5: Scraping Agendado (Cron)

Faz scraping em horários específicos.

### Trigger Configuration

- **Type**: Cron
- **Schedule**: `0 9 * * *` (Diariamente às 9h)

### Body da Requisição

```json
{
  "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
  "capturar_screenshots": true
}
```

---

## Workflow 6: Webhook - Receber URL e fazer Scraping

API n8n que recebe URL e faz scraping.

### Trigger: Webhook

- **HTTP Method**: POST
- **Path**: /scrape

### Request Body esperado

```json
{
  "product_url": "https://www.mercadolivre.com.br/..."
}
```

### Passos

1. **Webhook** - Recebe POST
2. **Set** - Prepara dados
3. **HTTP Request** - POST /scrape
4. **Respond to Webhook** - Retorna resultado

### Set Node (Preparar para scraping)

```json
{
  "url": "{{ $node[\"Webhook\"].json.product_url }}",
  "capturar_screenshots": true
}
```

### HTTP Request Node

```
Method: POST
URL: http://localhost:8000/scrape
Headers:
  Authorization: Bearer seu_token
Body: {{ $node[\"Set\"].json }}
```

### Respond to Webhook

```json
{
  "sucesso": "{{ $node[\"HTTP Request\"].json.sucesso }}",
  "dados": "{{ $node[\"HTTP Request\"].json.dados }}",
  "timestamp": "{{ new Date().toISOString() }}"
}
```

---

## Workflow 7: Enviar Screenshots por Email

Faz scraping e envia screenshots por email.

### Passos

```
HTTP Request (Scraping)
        ↓
    IF (sucesso && tem screenshots)
        ↓
    Email (Enviar screenshots)
```

### Email Node Configuration

**To**: seu_email@exemplo.com

**Subject**: 
```
Scraping concluído: {{ $node["HTTP Request"].json.dados.titulo }}
```

**Body (HTML)**:
```html
<h2>{{ $node["HTTP Request"].json.dados.titulo }}</h2>
<p>Scraping realizado em: {{ $node["HTTP Request"].json.timestamp }}</p>
<h3>Características:</h3>
<ul>
  <!-- Usar Function node para gerar lista -->
</ul>
```

**Attachments**: URLs dos screenshots

---

## Workflow 8: Slack Notification

Notifica um canal Slack com os dados extraídos.

### Slack Node Configuration

**Channel**: #mercado-livre-scraper

**Message**:
```
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Novo Produto Scraped*\n*Título:* {{ $node[\"HTTP Request\"].json.dados.titulo }}\n*Cor:* {{ $node[\"HTTP Request\"].json.dados.cor }}\n*Timestamp:* {{ $node[\"HTTP Request\"].json.timestamp }}"
  }
}
```

---

## Workflow 9: Google Sheets - Salvar Dados

Salva dados de scraping em Google Sheets.

### Passos

```
HTTP Request (Scraping)
        ↓
    IF (sucesso)
        ↓
    Google Sheets (Append Row)
```

### Google Sheets Node

**Sheet**: Dados de Produtos
**Values**:
```
[
  "{{ $node[\"HTTP Request\"].json.dados.titulo }}",
  "{{ $node[\"HTTP Request\"].json.dados.cor }}",
  "{{ JSON.stringify($node[\"HTTP Request\"].json.dados.bullet_points) }}",
  "{{ JSON.stringify($node[\"HTTP Request\"].json.dados.caracteristicas) }}",
  "{{ $node[\"HTTP Request\"].json.timestamp }}"
]
```

---

## Workflow 10: Complexo - Multi-ferramenta

Faz tudo: scraping, salva em BD, envia email e Slack.

### Fluxo

```
Trigger (Webhook)
        ↓
    HTTP Request (Scraping)
        ↓
    IF (sucesso)
    ↙    ↓    ↘
  BD  Email  Slack
    ↘    ↓    ↙
    Respond to Webhook
```

### IF Condition

```javascript
{{ $node["HTTP Request"].json.sucesso === true }}
```

---

## 🔑 Variáveis Úteis para n8n

### Headers Authentication

```javascript
{
  "Authorization": "Bearer seu_token_secreto_super_seguro_aqui",
  "Content-Type": "application/json"
}
```

### Body Template

```javascript
{
  "url": "{{ $node[\"trigger\"].json.product_url || 'https://...' }}",
  "capturar_screenshots": true
}
```

### Extrair Dados

```javascript
// Título
$node["HTTP Request"].json.dados.titulo

// Todas as características
$node["HTTP Request"].json.dados.caracteristicas

// Screenshot da página completa
$node["HTTP Request"].json.dados.screenshots.pagina_completa

// Verificar sucesso
$node["HTTP Request"].json.sucesso
```

---

## 📝 Dicas de Implementação

### 1. Usar Expression Builder

```
Click em: 123
Select: $node...
Choose: HTTP Request
Pick: json.dados.titulo
```

### 2. Converter para JSON válido

Se tiver erros de JSON:
```
Usar Function node:
return JSON.parse(input[0].json.dados.caracteristicas)
```

### 3. Limpar dados extras

```javascript
// Remove valores vazios
Object.keys(obj).forEach(key => {
  if (!obj[key]) delete obj[key];
});
return obj;
```

### 4. Tratamento de Timeout

Aumentar timeout no n8n:
- HTTP Request Node
- Settings
- Timeout: 120000 ms

---

## 🚀 Importar Workflow

1. No n8n, clique em **Workflows**
2. Clique em **Import**
3. Cole o JSON do workflow
4. Edite as variáveis (token, URLs)
5. Salve e execute

---

**Versão**: 1.0.0  
**Data**: 17 de novembro de 2025
