from pathlib import Path

def cargar_tickers_desde_txt():
    file_path = Path(__file__).resolve().parent.parent / "data" / "tickers.txt"
    print(f"📄 Cargando tickers desde: {file_path}")
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]
