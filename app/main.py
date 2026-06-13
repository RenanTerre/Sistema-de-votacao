import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.dto import VotoDTO
from app.services import SistemaDistribuidoService

app = FastAPI(title="Sistema de Votação Distribuída")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mapeia a pasta de arquivos estáticos
os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

servico_sistema = SistemaDistribuidoService()


@app.get("/", response_class=HTMLResponse)
async def raiz():
    caminho_html = os.path.join(BASE_DIR, "templates", "index.html")
    if not os.path.exists(caminho_html):
        caminho_html = os.path.join(BASE_DIR, "index.html")

    if not os.path.exists(caminho_html):
        raise HTTPException(status_code=404, detail="Arquivo index.html não foi encontrado.")

    return FileResponse(caminho_html)


@app.post("/votar")
async def votar(voto: VotoDTO):
    try:
        servico_sistema.enviar_voto_para_fila(voto.opcao)
        return {"status": "sucesso", "mensagem": f"Voto para '{voto.opcao}' enviado!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resultados")
async def obter_resultados():
    try:
        placar = servico_sistema.obtener_placar_cache()
        return placar
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))