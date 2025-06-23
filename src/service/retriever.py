import time
from pathlib import Path

import yfinance as yf
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# Ruta segura basada en el archivo actual
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ASSETS_FILE = DATA_DIR / "assets_info.json"
FAILED_FILE = DATA_DIR / "assets_fallidos.txt"
def safe_format(value, fallback="N/A", decimals=2, percentage=False):
    try:
        if value is None:
            return fallback
        if percentage:
            return f"{value * 100:.{decimals}f}%"
        if isinstance(value, (int, float)):
            return f"{value:,.{decimals}f}"
        return str(value)
    except:
        return fallback

def fetch_ticker_info(symbol):
    try:
        print(f"Procesando: {symbol}")
        time.sleep(0.3)  # Pausa para evitar throttling de Yahoo

        ticker = yf.Ticker(symbol)

        try:
            info = ticker.info or {}
        except:
            info = {}

        try:
            fast_info = ticker.fast_info or {}
        except:
            fast_info = {}

        if not info and not fast_info:
            raise ValueError("Sin datos disponibles")

        sector = info.get("sector", "N/A")
        industria = info.get("industry", "N/A")
        pais = info.get("country", "N/A")
        beta = info.get("beta") or fast_info.get("beta", 1)
        retorno = safe_format(info.get("fiveYearAvgDividendYield"), "0%", percentage=True)
        nombre = info.get("longName", symbol)
        descripcion = info.get("longBusinessSummary", f"{symbol} es un activo financiero relevante.")
        market_cap = safe_format(info.get("marketCap"), "Desconocida")
        dividendo = safe_format(info.get("dividendYield"), "0%", percentage=True)
        pe_ratio = safe_format(info.get("trailingPE"))

        riesgo = "Alto" if isinstance(beta, (int, float)) and beta > 1 else "Moderado"

        descripcion_completa = (
            f"{nombre} es una empresa del sector {sector}, industria {industria}, con sede en {pais}. "
            f"Capitalización bursátil estimada: {market_cap} USD. "
            f"Ratio P/E: {pe_ratio}, rendimiento por dividendo: {dividendo}. "
            f"{descripcion[:250]}"
        )

        return symbol, {
            "sector": sector,
            "industria": industria,
            "pais": pais,
            "riesgo": riesgo,
            "retorno_5a": retorno,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "dividendo": dividendo,
            "descripcion": descripcion_completa
        }

    except Exception as e:
        print(f"⚠️  {symbol}: {e}")
        return symbol, None



def build_asset_info(tickers):
    DATA_DIR.mkdir(exist_ok=True)
    data = {}
    errores = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_symbol = {executor.submit(fetch_ticker_info, symbol): symbol for symbol in tickers}
        for future in as_completed(future_to_symbol):
            symbol, result = future.result()
            if result:
                data[symbol] = result
            else:
                errores.append(symbol)

    with open(ASSETS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    if errores:
        with open(FAILED_FILE, "w") as f:
            f.write("\n".join(errores))
        print(f"⛔ Fallaron {len(errores)} tickers → guardados en {FAILED_FILE}")

    print(f"\n✅ Datos guardados: {len(data)} activos procesados.")