# src/cron_refresh_assets.py
from src.service.get_tickers_from_txt import cargar_tickers_desde_txt
from src.service.retriever import build_asset_info

if __name__ == "__main__":
    tickers = cargar_tickers_desde_txt()
    build_asset_info(tickers)
