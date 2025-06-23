import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.service.get_tickers_from_txt import cargar_tickers_desde_txt
from src.postDto import UserProfile
from src.service.retriever import build_asset_info
from src.service.gemini_agent import generar_recomendacion
from src.service.user_profile import generar_prompt_usuario
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ASSETS_PATH = Path(__file__).resolve().parent / "data" / "assets_info.json"

@app.post("/recomendar")
def recomendar(user: UserProfile):
    tickers = cargar_tickers_desde_txt()
    build_asset_info(tickers)

    with open(ASSETS_PATH, "r") as f:
        activos = json.load(f)

    prompt = generar_prompt_usuario(user.dict(), activos)
    raw_response = generar_recomendacion(prompt)

    # Limpiar bloque Markdown ```json ... ```
    json_text = re.sub(r"```json|```", "", raw_response).strip()

    try:
        parsed_response = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error al parsear JSON de Gemini: {str(e)}")

    return parsed_response