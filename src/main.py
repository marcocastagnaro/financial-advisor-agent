import json

from src.service.get_tickers_from_txt import cargar_tickers_desde_txt
from src.service.retriever import build_asset_info
from src.service.user_profile import generar_prompt_usuario
from src.service.gemini_agent import generar_recomendacion

if __name__ == "__main__":
    # Paso 1: Obtener activos si no los tenés
    tickers = cargar_tickers_desde_txt("data/tickers.txt")
    build_asset_info(tickers)
    # Paso 2: Cargar activos
    with open("data/assets_info.json", "r") as f:
        activos = json.load(f)

    # Paso 3: Simular perfil de usuario
    usuario = {
        "edad": 25,
        "ingresos": 500000,
        "riesgo": "Alta",
        "ocupacion": "Desarrollador de software",
        "descripcion_personal": "Interesado en tecnología, con conocimientos financieros básicos. Busca hacer crecer su capital a largo plazo.",
        "objetivo": "Invertir para alcanzar independencia financiera en 10 años",
        "horizonte_inversion": "largo plazo",  # largo plazo, mediano plazo, corto plazo
        "experiencia_inversion": "Intermedia",  # Básica / Intermedia / Avanzada
        "intereses": ["tecnología", "salud", "energía renovable"]
    }
    # Paso 4: Generar prompt y obtener respuesta
    prompt = generar_prompt_usuario(usuario, activos)
    resultado = generar_recomendacion(prompt)

    print("\n🔍 Recomendación del agente:\n")
    print(resultado)
