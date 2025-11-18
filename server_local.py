"""
Servidor Flask Local para Scraping via Webhook
Recebe requisições do n8n, faz scraping real e retorna dados

Como usar:
1. pip install flask flask-cors
2. python server_local.py
3. ngrok http 5000 (em outro terminal)
4. Use a URL do ngrok no n8n
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from scraping_mercado_livre_v2 import scrape_mercado_livre

app = Flask(__name__)
CORS(app)  # Permitir requisições do n8n

# Versão da API
API_VERSION = "1.0.0"


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de verificação de saúde"""
    return jsonify({
        "status": "ok",
        "service": "Scraping API Local",
        "version": API_VERSION
    }), 200


@app.route('/scrape', methods=['POST'])
def scrape():
    """
    Endpoint principal para scraping
    
    Recebe:
    {
        "url": "https://www.mercadolivre.com.br/...",
        "capturar_screenshots": false
    }
    
    Retorna:
    {
        "sucesso": true,
        "mensagem": "Scraping realizado com sucesso",
        "dados": {
            "titulo": "...",
            "bullet_points": [...],
            "caracteristicas": {...},
            "cor": "...",
            "descricao": "...",
            "screenshots": {},
            "debug_logs": [...]
        },
        "timestamp": "2025-11-18T..."
    }
    """
    try:
        # Validar request
        if not request.is_json:
            return jsonify({
                "sucesso": False,
                "mensagem": "Content-Type deve ser application/json",
                "dados": None
            }), 400
        
        data = request.get_json()
        url = data.get('url')
        capturar_screenshots = data.get('capturar_screenshots', False)
        
        # Validar URL
        if not url:
            return jsonify({
                "sucesso": False,
                "mensagem": "URL é obrigatória",
                "dados": None
            }), 400
        
        if not url.startswith('https://www.mercadolivre.com.br'):
            return jsonify({
                "sucesso": False,
                "mensagem": "URL deve ser do Mercado Livre",
                "dados": None
            }), 400
        
        print(f"\n{'='*80}")
        print(f"📍 NOVA REQUISIÇÃO DE SCRAPING")
        print(f"URL: {url}")
        print(f"Screenshots: {capturar_screenshots}")
        print(f"{'='*80}\n")
        
        # Executar scraping
        dados = scrape_mercado_livre(url, capturar_screenshots=capturar_screenshots)
        
        # Montar resposta
        resposta = {
            "sucesso": True,
            "mensagem": "Scraping realizado com sucesso",
            "dados": dados,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n✅ Scraping concluído com sucesso!")
        print(f"Dados retornados:")
        print(json.dumps(dados, ensure_ascii=False, indent=2))
        print()
        
        return jsonify(resposta), 200
        
    except Exception as e:
        print(f"\n❌ ERRO durante scraping: {e}\n")
        import traceback
        traceback.print_exc()
        return jsonify({
            "sucesso": False,
            "mensagem": f"Erro durante scraping: {str(e)}",
            "dados": None,
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/test', methods=['GET'])
def test():
    """Endpoint de teste para validar o servidor"""
    return jsonify({
        "status": "ok",
        "mensagem": "Servidor está funcionando!",
        "como_usar": {
            "endpoint": "/scrape",
            "metodo": "POST",
            "exemplo_request": {
                "url": "https://www.mercadolivre.com.br/panificadora-19-programas-gallant-600w-branca/p/MLB44589848",
                "capturar_screenshots": False
            }
        }
    }), 200


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 SERVIDOR DE SCRAPING LOCAL INICIADO")
    print("="*80)
    print("\n📌 Endpoints disponíveis:")
    print("   - GET  /health       → Verificar saúde do servidor")
    print("   - GET  /test         → Testar servidor")
    print("   - POST /scrape       → Fazer scraping (webhook do n8n)")
    print("\n🔗 Para expor localmente com ngrok:")
    print("   ngrok http 5000")
    print("\n💡 Cole a URL do ngrok no n8n como:")
    print("   https://xxxxx-xx-xx-ngrok.io/scrape")
    print("\n📚 Exemplo de requisição (POST):")
    print("   {")
    print('       "url": "https://www.mercadolivre.com.br/...",')
    print('       "capturar_screenshots": false')
    print("   }")
    print("\n" + "="*80 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
