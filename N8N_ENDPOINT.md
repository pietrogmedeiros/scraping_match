# 🔗 Documentação de Endpoint para n8n

## Configuração do HTTP Request no n8n

### 📌 Endpoint Principal - POST /scrape

#### URL
```
POST http://localhost:8000/scrape
```

Ou com Vercel:
```
POST https://seu-projeto.vercel.app/scrape
```

#### Autenticação (OBRIGATÓRIO)

**Header:**
```
Authorization: Bearer seu_token_secreto_super_seguro_aqui
```

#### Content-Type
```
application/json
```

---

## 🔧 Configuração no n8n

### Passo 1: Adicionar node "HTTP Request"

1. Abrir workflow do n8n
2. Clique em "+" para adicionar node
3. Procure por "HTTP Request"
4. Selecione "HTTP Request"

### Passo 2: Configurar o node

#### 2.1 Método
```
POST
```

#### 2.2 URL
```
http://localhost:8000/scrape
```

ou

```
https://seu-projeto.vercel.app/scrape
```

#### 2.3 Headers
Clique em "Add Header" e adicione:

| Header | Value |
|--------|-------|
| Authorization | Bearer seu_token_secreto_super_seguro_aqui |
| Content-Type | application/json |

**Na interface do n8n:**
```
Name: Authorization
Value: Bearer seu_token_secreto_super_seguro_aqui

Name: Content-Type
Value: application/json
```

#### 2.4 Body (JSON)

Clique em "Body" e selecione "JSON"

```json
{
  "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
  "capturar_screenshots": true
}
```

---

## 📝 Parâmetros Detalhados

### Request Body

```json
{
  "url": "string (obrigatório)",
  "capturar_screenshots": "boolean (opcional, padrão: true)"
}
```

#### Parâmetro: url
- **Tipo**: string
- **Obrigatório**: Sim
- **Descrição**: URL completa do produto no Mercado Livre
- **Exemplo**: `https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848`
- **Validação**: Deve conter `mercadolivre.com.br`

#### Parâmetro: capturar_screenshots
- **Tipo**: boolean
- **Obrigatório**: Não
- **Padrão**: true
- **Descrição**: Se deve capturar screenshots durante o scraping
- **Valores**: `true` ou `false`

---

## 📤 Response (Sucesso - 200)

```json
{
  "sucesso": true,
  "mensagem": "Scraping realizado com sucesso",
  "dados": {
    "titulo": "Panificadora 19 Programas Gallant 600w Branca",
    "bullet_points": [
      "Quantidade de programas:",
      "Com janela de visualização:",
      "Capacidade de pão:",
      "Com temporizador:",
      "Com display digital:"
    ],
    "caracteristicas": {
      "Capacidade de pão": "1 kg",
      "Com display digital": "Sim",
      "Com janela de visualização": "Sim",
      "Quantidade de programas": "19",
      "Com temporizador": "Sim"
    },
    "cor": "Branca",
    "descricao": "Nada melhor do que apreciar o cheiro irresistível de pão fresco pela manhã...",
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

---

## ❌ Respostas de Erro

### 401 - Token Inválido ou Ausente

```json
{
  "detail": "Token inválido"
}
```

**Status Code**: 401

**Solução**: Verificar se o token está correto no header Authorization

### 400 - URL Inválida

```json
{
  "detail": "URL deve ser de um produto do Mercado Livre"
}
```

**Status Code**: 400

**Solução**: Usar URL de um produto válido do Mercado Livre (mercadolivre.com.br)

### 500 - Erro Interno

```json
{
  "sucesso": false,
  "mensagem": "Erro durante scraping: mensagem de erro específica",
  "timestamp": "2025-11-17T19:37:22.123456"
}
```

**Status Code**: 500

**Solução**: Verificar logs da API ou tentar novamente

---

## 🎯 Exemplo Completo no n8n

### Configuração Visual

```
┌─────────────────────────────────────────┐
│         HTTP Request                    │
├─────────────────────────────────────────┤
│ Method:          POST                   │
│ URL:             http://localhost:8000/scrape │
├─────────────────────────────────────────┤
│ Headers:                                │
│ ✓ Authorization: Bearer seu_token       │
│ ✓ Content-Type: application/json        │
├─────────────────────────────────────────┤
│ Body (JSON):                            │
│ {                                       │
│   "url": "https://...",                 │
│   "capturar_screenshots": true          │
│ }                                       │
├─────────────────────────────────────────┤
│ Response Type: JSON                     │
│ ✓ Treat as File: OFF                    │
│ ✓ Timeout: 120 (segundos)               │
└─────────────────────────────────────────┘
```

---

## 💾 Usando a Resposta no n8n

Após o HTTP Request, você pode acessar os dados da resposta:

### Acessar campos específicos

```javascript
// Título do produto
{{ $node["HTTP Request"].json.dados.titulo }}

// Características
{{ $node["HTTP Request"].json.dados.caracteristicas }}

// URLs dos screenshots
{{ $node["HTTP Request"].json.dados.screenshots.pagina_completa }}

// Status de sucesso
{{ $node["HTTP Request"].json.sucesso }}
```

### Exemplo de uso em outro node

**Set node para extrair dados:**

```json
{
  "titulo": "{{ $node[\"HTTP Request\"].json.dados.titulo }}",
  "bullet_points": "{{ $node[\"HTTP Request\"].json.dados.bullet_points }}",
  "screenshots": "{{ $node[\"HTTP Request\"].json.dados.screenshots }}",
  "timestamp": "{{ $node[\"HTTP Request\"].json.timestamp }}"
}
```

---

## 🔄 Workflow Exemplo no n8n

```
Trigger (Manual/Cron)
        ↓
    ┌───────────────────┐
    │  Set Variables    │
    │  (URL do produto) │
    └───────────────────┘
        ↓
    ┌───────────────────┐
    │  HTTP Request     │
    │  POST /scrape     │
    └───────────────────┘
        ↓
    ┌───────────────────┐
    │  IF (sucesso?)    │
    └───────────────────┘
        ↙           ↘
      SIM           NÃO
        ↓             ↓
    ┌─────────┐   ┌──────────┐
    │ Extract │   │Send Error│
    │ Data    │   │Notification│
    └─────────┘   └──────────┘
        ↓
    ┌───────────────────┐
    │  Save to Database │
    │  or Send Email    │
    └───────────────────┘
```

---

## 📋 Checklist para n8n

- [ ] URL da API configurada
- [ ] Token Bearer correto no header Authorization
- [ ] Content-Type definido como application/json
- [ ] Body em JSON válido
- [ ] Timeout em 120 segundos (mínimo)
- [ ] Resposta parseada como JSON
- [ ] Tratamento de erros (status 400, 401, 500)
- [ ] Variáveis dinamicamente vinculadas (se necessário)

---

## ⚠️ Troubleshooting n8n

### Erro: "401 Unauthorized"

**Problema**: Token inválido
**Solução**:
```
1. Verificar se o token está correto
2. Confirmar que está no formato: Bearer <token>
3. Verificar espaços em branco extras
```

### Erro: "Connection refused"

**Problema**: API não está rodando
**Solução**:
```
1. Iniciar a API: python api.py
2. Verificar se está em http://localhost:8000
3. Se usar Vercel, usar: https://seu-projeto.vercel.app
```

### Erro: "Timeout"

**Problema**: Scraping demorando muito
**Solução**:
```
1. Aumentar timeout em n8n para 120s+
2. Verificar conexão de internet
3. Tentar com URL diferente
```

### Erro: "Invalid JSON"

**Problema**: Body malformado
**Solução**:
```
1. Verificar se JSON está válido
2. Usar JSON format: {"key":"value"}
3. Não deixar vírgulas extras
```

---

## 🚀 Deployment com Vercel

Quando fazer deploy na Vercel, mudar a URL:

### Local
```
http://localhost:8000/scrape
```

### Vercel
```
https://seu-projeto.vercel.app/scrape
```

E adicionar o token no Vercel (Environment Variables):
```
API_TOKEN=seu_token_secreto_super_seguro_aqui
```

---

## 📊 Dados Retornados - Referência Completa

| Campo | Tipo | Descrição |
|-------|------|-----------|
| sucesso | boolean | Indica se o scraping foi bem-sucedido |
| mensagem | string | Mensagem descritiva do resultado |
| dados | object | Objeto com todos os dados extraídos |
| dados.titulo | string | Título do produto |
| dados.bullet_points | array | Array de pontos-chave do produto |
| dados.caracteristicas | object | Chave-valor com características |
| dados.cor | string | Cor do produto (ou "N/A") |
| dados.descricao | string | Descrição completa do produto |
| dados.screenshots | object | URLs dos screenshots capturados |
| timestamp | string | ISO 8601 timestamp da requisição |

---

## 💡 Dicas Úteis

### 1. Usar variáveis no n8n

```javascript
// URL dinâmica de um node anterior
{{ $node["trigger"].json.product_url }}

// Usar em outras requisições
{{ $node["HTTP Request"].json.dados.titulo }}
```

### 2. Tratamento de erros

```javascript
// Verificar se o scraping foi bem-sucedido
{{ $node["HTTP Request"].json.sucesso === true }}

// Pegar mensagem de erro
{{ $node["HTTP Request"].json.mensagem }}
```

### 3. Iterar sobre características

No n8n, usar "Function" node:

```javascript
return $node["HTTP Request"].json.dados.caracteristicas;
```

Depois usar "Item Lists" para processar cada uma

### 4. Processar screenshots

```javascript
// Pegar todas as URLs de screenshots
Object.values($node["HTTP Request"].json.dados.screenshots)

// Baixar screenshots
// Usar outro HTTP Request com: /screenshot/{filename}
```

---

## 🔗 Links Úteis

- API Local: http://localhost:8000/docs
- Documentação Swagger: http://localhost:8000/docs
- GitHub: [seu repositório]
- n8n Docs: https://docs.n8n.io/

---

**Versão**: 1.0.0  
**Data**: 17 de novembro de 2025  
**Status**: Pronto para n8n ✅
