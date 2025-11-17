# Exemplos de Uso da API

## Python com requests

```python
import requests
import json

# Configurações
API_URL = "http://localhost:8000"  # ou sua URL da Vercel
API_TOKEN = "seu_token_secreto_super_seguro_aqui"

# Headers de autenticação
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Dados do produto
data = {
    "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
    "capturar_screenshots": True
}

# Fazer requisição
try:
    response = requests.post(
        f"{API_URL}/scrape",
        headers=headers,
        json=data,
        timeout=120
    )
    
    resultado = response.json()
    
    if resultado["sucesso"]:
        print("✅ Scraping realizado com sucesso!")
        print(f"Título: {resultado['dados']['titulo']}")
        print(f"Screenshots capturados:")
        for tipo, url in resultado['dados']['screenshots'].items():
            print(f"  - {tipo}: {url}")
    else:
        print(f"❌ Erro: {resultado['mensagem']}")
        
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
```

## JavaScript/Node.js com fetch

```javascript
const API_URL = "http://localhost:8000"; // ou sua URL da Vercel
const API_TOKEN = "seu_token_secreto_super_seguro_aqui";

async function scrapeProduct(url) {
    try {
        const response = await fetch(`${API_URL}/scrape`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${API_TOKEN}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url,
                capturar_screenshots: true
            })
        });

        const resultado = await response.json();

        if (resultado.sucesso) {
            console.log("✅ Scraping realizado com sucesso!");
            console.log("Título:", resultado.dados.titulo);
            console.log("Screenshots capturados:");
            Object.entries(resultado.dados.screenshots).forEach(([tipo, url]) => {
                console.log(`  - ${tipo}: ${url}`);
            });
        } else {
            console.log("❌ Erro:", resultado.mensagem);
        }

        return resultado;
    } catch (error) {
        console.error("Erro na requisição:", error);
    }
}

// Usar a função
scrapeProduct("https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848");
```

## cURL

```bash
# Básico
curl -X POST http://localhost:8000/scrape \
  -H "Authorization: Bearer seu_token_secreto_super_seguro_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
    "capturar_screenshots": true
  }'

# Com pretty print JSON
curl -X POST http://localhost:8000/scrape \
  -H "Authorization: Bearer seu_token_secreto_super_seguro_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
    "capturar_screenshots": true
  }' | jq .

# Salvar resposta em arquivo
curl -X POST http://localhost:8000/scrape \
  -H "Authorization: Bearer seu_token_secreto_super_seguro_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
    "capturar_screenshots": true
  }' > resultado.json

# Baixar screenshot
curl -O -H "Authorization: Bearer seu_token_secreto_super_seguro_aqui" \
  http://localhost:8000/screenshot/20251117_194548_01_pagina_completa.png
```

## Postman

### Configuração

1. **Nova Request**
   - Método: POST
   - URL: http://localhost:8000/scrape (ou sua URL da Vercel)

2. **Headers**
   - Authorization: Bearer seu_token_secreto_super_seguro_aqui
   - Content-Type: application/json

3. **Body (JSON)**
```json
{
  "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
  "capturar_screenshots": true
}
```

4. **Enviar**

## PowerShell

```powershell
$ApiUrl = "http://localhost:8000"
$ApiToken = "seu_token_secreto_super_seguro_aqui"
$ProductUrl = "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848"

$headers = @{
    "Authorization" = "Bearer $ApiToken"
    "Content-Type" = "application/json"
}

$body = @{
    "url" = $ProductUrl
    "capturar_screenshots" = $true
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "$ApiUrl/scrape" -Method POST -Headers $headers -Body $body

$resultado = $response.Content | ConvertFrom-Json

if ($resultado.sucesso) {
    Write-Host "✅ Scraping realizado com sucesso!"
    Write-Host "Título: $($resultado.dados.titulo)"
    Write-Host "Screenshots capturados:"
    $resultado.dados.screenshots | ForEach-Object {
        $_.PSObject.Properties | ForEach-Object {
            Write-Host "  - $($_.Name): $($_.Value)"
        }
    }
} else {
    Write-Host "❌ Erro: $($resultado.mensagem)"
}
```

## Go

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type ScrapeRequest struct {
	URL                 string `json:"url"`
	CapturarScreenshots bool   `json:"capturar_screenshots"`
}

type ScrapeResponse struct {
	Sucesso   bool                   `json:"sucesso"`
	Mensagem  string                 `json:"mensagem"`
	Dados     map[string]interface{} `json:"dados"`
	Timestamp string                 `json:"timestamp"`
}

func main() {
	apiURL := "http://localhost:8000"
	apiToken := "seu_token_secreto_super_seguro_aqui"
	productURL := "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848"

	// Preparar requisição
	reqBody := ScrapeRequest{
		URL:                 productURL,
		CapturarScreenshots: true,
	}

	jsonData, _ := json.Marshal(reqBody)
	req, _ := http.NewRequest("POST", fmt.Sprintf("%s/scrape", apiURL), bytes.NewBuffer(jsonData))

	// Headers
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", apiToken))
	req.Header.Set("Content-Type", "application/json")

	// Fazer requisição
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Erro na requisição:", err)
		return
	}
	defer resp.Body.Close()

	// Processar resposta
	body, _ := ioutil.ReadAll(resp.Body)
	var result ScrapeResponse
	json.Unmarshal(body, &result)

	if result.Sucesso {
		fmt.Println("✅ Scraping realizado com sucesso!")
		fmt.Printf("Título: %v\n", result.Dados["titulo"])
		fmt.Println("Screenshots capturados:")
		if screenshots, ok := result.Dados["screenshots"].(map[string]interface{}); ok {
			for tipo, url := range screenshots {
				fmt.Printf("  - %s: %v\n", tipo, url)
			}
		}
	} else {
		fmt.Printf("❌ Erro: %s\n", result.Mensagem)
	}
}
```

## Java

```java
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

public class MercadoLivreScraper {
    public static void main(String[] args) throws IOException, InterruptedException {
        String apiUrl = "http://localhost:8000";
        String apiToken = "seu_token_secreto_super_seguro_aqui";
        String productUrl = "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848";

        // Preparar JSON
        JsonObject jsonBody = new JsonObject();
        jsonBody.addProperty("url", productUrl);
        jsonBody.addProperty("capturar_screenshots", true);

        // Criar requisição
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(apiUrl + "/scrape"))
                .header("Authorization", "Bearer " + apiToken)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody.toString()))
                .build();

        // Fazer requisição
        HttpClient client = HttpClient.newHttpClient();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        // Processar resposta
        Gson gson = new Gson();
        JsonObject result = gson.fromJson(response.body(), JsonObject.class);

        if (result.get("sucesso").getAsBoolean()) {
            System.out.println("✅ Scraping realizado com sucesso!");
            System.out.println("Título: " + result.getAsJsonObject("dados").get("titulo"));
        } else {
            System.out.println("❌ Erro: " + result.get("mensagem"));
        }
    }
}
```

## PHP

```php
<?php

$apiUrl = "http://localhost:8000";
$apiToken = "seu_token_secreto_super_seguro_aqui";
$productUrl = "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848";

// Preparar dados
$data = array(
    "url" => $productUrl,
    "capturar_screenshots" => true
);

// Fazer requisição
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $apiUrl . "/scrape");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    "Authorization: Bearer " . $apiToken,
    "Content-Type: application/json"
));

$response = curl_exec($ch);
curl_close($ch);

// Processar resposta
$result = json_decode($response, true);

if ($result["sucesso"]) {
    echo "✅ Scraping realizado com sucesso!\n";
    echo "Título: " . $result["dados"]["titulo"] . "\n";
    echo "Screenshots capturados:\n";
    foreach ($result["dados"]["screenshots"] as $tipo => $url) {
        echo "  - " . $tipo . ": " . $url . "\n";
    }
} else {
    echo "❌ Erro: " . $result["mensagem"] . "\n";
}

?>
```

## Ruby

```ruby
require 'net/http'
require 'json'
require 'uri'

api_url = "http://localhost:8000"
api_token = "seu_token_secreto_super_seguro_aqui"
product_url = "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848"

# Preparar dados
data = {
  url: product_url,
  capturar_screenshots: true
}

# Fazer requisição
uri = URI("#{api_url}/scrape")
http = Net::HTTP.new(uri.host, uri.port)
request = Net::HTTP::Post.new(uri.path, {
  'Authorization' => "Bearer #{api_token}",
  'Content-Type' => 'application/json'
})
request.body = data.to_json

response = http.request(request)
result = JSON.parse(response.body)

# Processar resposta
if result['sucesso']
  puts "✅ Scraping realizado com sucesso!"
  puts "Título: #{result['dados']['titulo']}"
  puts "Screenshots capturados:"
  result['dados']['screenshots'].each do |tipo, url|
    puts "  - #{tipo}: #{url}"
  end
else
  puts "❌ Erro: #{result['mensagem']}"
end
```

## Gerar Token Seguro

Para gerar um token seguro e aleatório:

### Python
```python
import secrets
token = secrets.token_urlsafe(32)
print(f"API_TOKEN={token}")
```

### Bash
```bash
openssl rand -hex 32
# ou
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### JavaScript
```javascript
const token = require('crypto').randomBytes(32).toString('hex');
console.log(`API_TOKEN=${token}`);
```

---

**Dica**: Sempre use tokens fortes e aleatórios em produção!
