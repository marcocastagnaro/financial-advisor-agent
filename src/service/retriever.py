import yfinance as yf
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_ticker_info(symbol):
    try:
        print(f"Procesando: {symbol} (tipo: {type(symbol)})")
        ticker = yf.Ticker(symbol)

        # Intentar primero con .info
        try:
            info = ticker.info
        except Exception:
            info = {}

        # Fallback a .fast_info
        fast_info = {}
        try:
            fast_info = ticker.fast_info
        except:
            pass

        # Verificación mínima
        if not info and not fast_info:
            raise ValueError("Datos no disponibles o protegidos")

        sector = info.get("sector") or "N/A"
        beta = info.get("beta") or fast_info.get("beta") or 1
        riesgo = "Alto" if beta > 1 else "Moderado"
        retorno = info.get("fiveYearAvgDividendYield") or 0
        descripcion = info.get("longBusinessSummary") or f"{symbol} es un activo financiero relevante."
        nombre = info.get("longName") or symbol
        industria = info.get("industry") or "N/A"
        pais = info.get("country") or "N/A"
        market_cap = info.get("marketCap")
        dividendo = info.get("dividendYield")
        pe_ratio = info.get("trailingPE")

        descripcion_completa = (
            f"{nombre} es una empresa del sector {sector}, industria {industria}, con sede en {pais}. "
            f"Capitalización bursátil estimada: {market_cap:,} USD. "
            f"Ratio P/E: {pe_ratio}, rendimiento por dividendo: {dividendo}. "
            f"{descripcion[:250]}"
        )
        return symbol, {
            "sector": sector,
            "industria": industria,
            "pais": pais,
            "riesgo": riesgo,
            "retorno_5a": f"{retorno * 100:.2f}%",
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "dividendo": dividendo,
            "descripcion": descripcion_completa
        }

    except Exception as e:
        print(f"⚠️  {symbol}: {e}")
        return symbol, None


def build_asset_info(tickers):
    os.makedirs("../data", exist_ok=True)
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

    with open("../data/assets_info.json", "w") as f:
        json.dump(data, f, indent=2)

    if errores:
        with open("../data/assets_fallidos.txt", "w") as f:
            f.write("\n".join(errores))
        print(f"⛔ Fallaron {len(errores)} tickers → guardados en data/assets_fallidos.txt")

    print(f"\n✅ Datos guardados: {len(data)} activos procesados.")
