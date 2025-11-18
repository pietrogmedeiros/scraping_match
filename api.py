from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import json
import shutil
from datetime import datetime
from pydantic import BaseModel
from dotenv import load_dotenv
from scraping_mercado_livre_v2 import scrape_mercado_livre
import logging

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="Mercado Livre Scraper API",
    description="API para scraping de produtos do Mercado Livre",
    version="1.0.0"
)

# Token de autenticação
# Usar token fixo para testes até conseguir ler variável de ambiente corretamente
API_TOKEN = "6eOvzj_mCgrI83_7SqU-_JdGCMZk3Q9WjIw1A7e9ZPs"
# API_TOKEN = os.getenv("API_TOKEN", "seu_token_secreto_aqui")
logger.info(f"API_TOKEN configurado manualmente")

# Modelo de requisição
class ScrapeRequest(BaseModel):
    url: str
    capturar_screenshots: bool = True


class ScrapeResponse(BaseModel):
    sucesso: bool
    mensagem: str
    dados: dict = None
    timestamp: str = None


def verificar_token(authorization: str = Header(None)):
    """Verifica se o token é válido"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    # Formato esperado: Bearer <token>
    partes = authorization.split(" ")
    if len(partes) != 2 or partes[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Formato de autenticação inválido. Use: Bearer <token>")
    
    token = partes[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return token


def limpar_screenshots_antigos(dias=7):
    """Remove screenshots com mais de X dias"""
    try:
        screenshots_dir = "screenshots"
        if os.path.exists(screenshots_dir):
            agora = datetime.now().timestamp()
            for arquivo in os.listdir(screenshots_dir):
                caminho_arquivo = os.path.join(screenshots_dir, arquivo)
                tempo_arquivo = os.path.getmtime(caminho_arquivo)
                idade_dias = (agora - tempo_arquivo) / (24 * 3600)
                
                if idade_dias > dias:
                    try:
                        os.remove(caminho_arquivo)
                        logger.info(f"Screenshot antigo removido: {arquivo}")
                    except Exception as e:
                        logger.error(f"Erro ao remover screenshot: {e}")
    except Exception as e:
        logger.error(f"Erro ao limpar screenshots antigos: {e}")


@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar a API"""
    logger.info("API iniciada com sucesso")
    logger.info(f"Token de autenticação configurado: {bool(API_TOKEN)}")


@app.get("/", tags=["Info"])
async def root():
    """Retorna informações da API"""
    return {
        "nome": "Mercado Livre Scraper API",
        "versao": "1.0.0",
        "descricao": "API para scraping de produtos do Mercado Livre",
        "endpoints": {
            "POST /scrape": "Realizar scraping de um produto",
            "GET /status": "Verificar status da API",
            "GET /screenshot/{filename}": "Baixar um screenshot capturado"
        },
        "autenticacao": "Use header: Authorization: Bearer <seu_token>"
    }


@app.get("/status", tags=["Info"])
async def status():
    """Verifica status da API"""
    screenshots_count = 0
    screenshots_dir = "screenshots"
    if os.path.exists(screenshots_dir):
        screenshots_count = len(os.listdir(screenshots_dir))
    
    return {
        "online": True,
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "screenshots_armazenados": screenshots_count
    }


@app.post("/scrape", tags=["Scraping"], response_model=ScrapeResponse)
async def scrape_produto(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks,
    authorization: str = Header(None)
):
    """
    Realiza scraping de um produto do Mercado Livre
    
    Requer autenticação via token no header Authorization
    
    Exemplo:
    ```
    POST /scrape
    Authorization: Bearer seu_token_aqui
    
    {
        "url": "https://www.mercadolivre.com.br/produto/...",
        "capturar_screenshots": true
    }
    ```
    """
    try:
        # Verificar token
        verificar_token(authorization)
        
        # Validar URL
        if not request.url:
            raise HTTPException(status_code=400, detail="URL não fornecida")
        
        if "mercadolivre.com.br" not in request.url:
            raise HTTPException(
                status_code=400,
                detail="URL deve ser de um produto do Mercado Livre"
            )
        
        logger.info(f"Iniciando scraping de: {request.url}")
        
        # Executar scraping
        try:
            dados = scrape_mercado_livre(
                url=request.url,
                capturar_screenshots=request.capturar_screenshots
            )
        except TypeError as te:
            logger.error(f"Erro de tipo ao chamar scrape_mercado_livre: {str(te)}")
            return ScrapeResponse(
                sucesso=False,
                mensagem=f"Erro ao chamar função de scraping: {str(te)}",
                timestamp=datetime.now().isoformat()
            )
        
        # Converter caminhos de screenshots para URLs acessíveis
        if dados["screenshots"]:
            for tipo, caminho in dados["screenshots"].items():
                if caminho and os.path.exists(caminho):
                    # Convertendo caminho para URL
                    nome_arquivo = os.path.basename(caminho)
                    dados["screenshots"][tipo] = f"/screenshot/{nome_arquivo}"
        
        # Agendar limpeza de screenshots antigos em background
        background_tasks.add_task(limpar_screenshots_antigos)
        
        logger.info("Scraping concluído com sucesso")
        
        return ScrapeResponse(
            sucesso=True,
            mensagem="Scraping realizado com sucesso",
            dados=dados,
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro durante scraping: {str(e)}")
        return ScrapeResponse(
            sucesso=False,
            mensagem=f"Erro durante scraping: {str(e)}",
            timestamp=datetime.now().isoformat()
        )


@app.get("/screenshot/{filename}", tags=["Recursos"])
async def download_screenshot(
    filename: str,
    authorization: str = Header(None)
):
    """
    Baixa um screenshot capturado
    
    Requer autenticação via token
    """
    try:
        # Verificar token
        verificar_token(authorization)
        
        # Validar nome do arquivo (segurança)
        if "/" in filename or "\\" in filename or ".." in filename:
            raise HTTPException(status_code=400, detail="Nome de arquivo inválido")
        
        caminho_arquivo = os.path.join("screenshots", filename)
        
        if not os.path.exists(caminho_arquivo):
            raise HTTPException(status_code=404, detail="Screenshot não encontrado")
        
        logger.info(f"Screenshot baixado: {filename}")
        
        return FileResponse(
            path=caminho_arquivo,
            media_type="image/png",
            filename=filename
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao baixar screenshot: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao baixar screenshot")


@app.get("/screenshots/list", tags=["Recursos"])
async def listar_screenshots(authorization: str = Header(None)):
    """
    Lista todos os screenshots disponíveis
    
    Requer autenticação via token
    """
    try:
        # Verificar token
        verificar_token(authorization)
        
        screenshots_dir = "screenshots"
        screenshots = []
        
        if os.path.exists(screenshots_dir):
            for arquivo in os.listdir(screenshots_dir):
                caminho_completo = os.path.join(screenshots_dir, arquivo)
                tamanho = os.path.getsize(caminho_completo)
                tempo_modificacao = os.path.getmtime(caminho_completo)
                
                screenshots.append({
                    "nome": arquivo,
                    "tamanho_bytes": tamanho,
                    "url": f"/screenshot/{arquivo}",
                    "data_criacao": datetime.fromtimestamp(tempo_modificacao).isoformat()
                })
        
        return {
            "total": len(screenshots),
            "screenshots": screenshots
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar screenshots: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar screenshots")


# Servir arquivos estáticos (screenshots)
try:
    if os.path.exists("screenshots"):
        app.mount("/static", StaticFiles(directory="screenshots"), name="static")
except Exception as e:
    logger.warning(f"Não foi possível montar diretório de screenshots: {e}")


# Tratamento de erro 404
@app.get("/{full_path:path}", tags=["Info"])
async def rota_nao_encontrada(full_path: str):
    """Trata rotas não encontradas"""
    return JSONResponse(
        status_code=404,
        content={
            "erro": "Rota não encontrada",
            "caminho": full_path,
            "dica": "Consulte GET / para ver as rotas disponíveis"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Determinar porta
    port = int(os.getenv("PORT", 8000))
    
    # Executar servidor
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Desabilitar reload para produção
        log_level="info"
    )
