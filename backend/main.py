from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
import random
from datetime import datetime

from detectors.bos_detector import detect_bos
from detectors.ob_detector import detect_order_blocks
from detectors.ta_detector import detect_ta_confirmation
from data.binance_client import BinanceClient
from data.price_cache import PriceCache

# Инициализация кэша
cache = PriceCache()
active_connections = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск фоновых задач
    binance_symbols = ["BTCUSDT", "ETHUSDT"]
    asyncio.create_task(BinanceClient().stream_klines(binance_symbols, "1m", handle_binance_kline))
    asyncio.create_task(generate_mock_prices())
    asyncio.create_task(signal_generator())
    yield
    # Очистка (если нужно)
    active_connections.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def handle_binance_kline(kline_data):
    symbol = kline_data["symbol"]
    cache.add_binance_kline(symbol, kline_data)

async def generate_mock_prices():
    base_prices = {"EUR_USD": 1.0800}
    while True:
        for symbol, base in base_prices.items():
            vol = 0.0005
            price = base + random.uniform(-vol, vol)
            cache.add_oanda_tick(symbol, price - 0.0001, price + 0.0001)
            base_prices[symbol] = price
        await asyncio.sleep(1)

async def broadcast_signal(signal: dict):
    if active_connections:
        message = json.dumps(signal)
        await asyncio.gather(
            *[conn.send_text(message) for conn in active_connections],
            return_exceptions=True
        )

async def signal_generator():
    assets = [
        {"pocket": "BTC/USD", "symbol": "BTCUSDT", "source": "binance"},
        {"pocket": "EUR/USD", "symbol": "EUR_USD", "source": "mock"},
    ]
    while True:
        for asset in assets:
            df_m5 = cache.get_dataframe(asset["symbol"], asset["source"], 'M1')
            df_h1 = cache.get_dataframe(asset["symbol"], asset["source"], 'H1')
            
            if df_m5.empty or len(df_m5) < 50 or df_h1.empty:
                continue

            trend = "uptrend" if len(df_h1) > 1 and df_h1['close'].iloc[-1] > df_h1['close'].iloc[-2] else "downtrend"
            bos = detect_bos(df_m5, trend=trend)
            obs = detect_order_blocks(df_m5)
            
            if bos and obs:
                signal_type = "CALL" if bos['type'] == "bullish_bos" else "PUT"
                ta_result = detect_ta_confirmation(df_m5, signal_type)
                if ta_result["confirmed"]:
                    ob = obs[0]
                    signal = {
                        "asset": asset["pocket"],
                        "type": signal_type,
                        "entry_zone": f"{ob['zone_low']:.4f}–{ob['zone_high']:.4f}",
                        "expiry_minutes": 4,
                        "expected_payout": 84,
                        "ta_details": ta_result["indicators"]
                    }
                    await broadcast_signal(signal)
        await asyncio.sleep(15)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # ← порт 8001