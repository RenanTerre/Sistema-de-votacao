import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.dto import VotoDTO
from app.services import SistemaDistribuidoService

app = FastAPI(title="Sistema de Votação Distribuída")

# Ativa o mapeamento para servir a imagem do QR Code salva na pasta /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração global de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

servico_sistema = SistemaDistribuidoService()


@app.get("/", response_class=HTMLResponse)
def raiz():
    """Entrega o ficheiro index.html direto pelo servidor do FastAPI"""
    caminho_html = os.path.join("templates", "index.html")

    if not os.path.exists(caminho_html):
        caminho_html = "index.html"

    with open(caminho_html, "r", encoding="utf-8") as file:
        return file.read()


@app.post("/votar")
def votar(voto: VotoDTO):
    try:
        # Envia para a fila do RabbitMQ
        servico_sistema.enviar_voto_para_fila(voto.opcao)
        return {
            "status": "sucesso",
            "mensagem": f"Voto para '{voto.opcao}' enviado com sucesso!",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao enviar voto para a fila: {str(e)}",
        )


@app.get("/resultados")
def obter_resultados():
    try:
        # Puxa o placar em tempo real do Redis
        placar = servico_sistema.obtener_placar_cache()
        return placar
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar resultados no Redis: {str(e)}",
        )